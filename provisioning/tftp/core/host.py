import time

from scrapli.driver.core import IOSXEDriver

from config import Config
from core.utils import is_online, render_file, load_yaml


class Host:
    c = Config()
    swversions: dict = c.swversions
    credentials: dict = c.credentials

    def __init__(self, ip: str, username: str, password: str, enable: str = None):
        self.ip = ip
        self.username: str = username
        self.password: str = password
        self.enable: str = enable
        self._conn: IOSXEDriver = None
        self.hostname: str = None
        self.platform: str = None
        self.version: str = None
        self.model: str = None
        self.serial: str = None
        self.interfaces: dict = None
        self.system_image: str = None
        self.bytes_free: int = None

    def connect(self, timeout_transport: float = 30) -> None:
        self._conn = IOSXEDriver(
            host=self.ip,
            auth_username=self.username,
            auth_password=self.password,
            auth_secondary=self.enable if self.enable else self.password,
            auth_strict_key=False,
            transport="ssh2",
            timeout_transport=timeout_transport,
        )
        self._conn.open()

    def disconnect(self):
        self._conn.close()

    def connection_alive(self) -> bool:
        if self._conn and self._conn.isalive():
            return True
        else:
            return False

    def get_device_details(self):
        if not self.connection_alive():
            self.connect()
        response = self._conn.send_command("show version").genie_parse_output()
        self.hostname = response["version"].get("hostname")
        self.platform = response["version"].get("platform")
        self.version = response["version"].get("version")
        self.model = response["version"].get("chassis")
        self.serial = response["version"].get("chassis_sn")
        self.interfaces = response["version"].get("number_of_intfs")
        self.system_image = response["version"].get("system_image")
        self.bytes_free = self._check_free_space()

    def _check_free_space(self):
        if not self.connection_alive():
            self.connect()
        response = self._conn.send_command("dir").genie_parse_output()
        return response["dir"]["flash:/"]["bytes_free"]

    def _upgrade_required(self) -> str:
        if self.platform is None:
            self.get_device_details()

        platform = self.swversions.get(self.platform.lower())

        if platform:
            return platform if platform["version"] != self.version else None
        else:
            raise ValueError("Unable to find device platform")

    def upgrade_device(self):
        attempts = 0
        while True:
            if attempts < 20:
                try:
                    self.connect(1200)
                    break
                except Exception:
                    time.sleep(1)
                    attempts += 1
            else:
                raise ConnectionError(f"Cannot connect to {self.ip}")

        new_image = self._upgrade_required()
        if new_image:
            print("saving config")
            self._conn.send_command("write memory")
            print("downloading image")
            self._conn.send_command(
                f"archive download-sw /reload /overwrite /imageonly http:/10.0.0.1/files/{new_image['image']}",
                timeout_ops=1200
            )

            print("download finished")
            self.disconnect()
            time.sleep(5)
            print("waiting for device to come back online")
            if is_online(self.ip):
                self.get_device_details()
                if not self._upgrade_required():
                    print("upgrade successful")
                else:
                    print("upgrade failed")
        else:
            print("upgrade not required")

    def send_config(self, config_type):
        if config_type == "initial":
            # self._conn.send_configs(config.split("\n"))
            pass
