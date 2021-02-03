from scrapli.driver.core import IOSXEDriver


class Host:
    def __init__(self, ip: str, username: str, password: str, enable: str = None):
        self.ip = ip
        self.username: str = username
        self.password: str = password
        self.enable: str = enable
        self._conn: IOSXEDriver = None
        self.platform: str = None
        self.version: str = None
        self.model: str = None
        self.serial: str = None
        self.interfaces: dict = None
        self.system_image: str = None
        self.bytes_free: int = None

    def connect(self) -> None:
        self._conn = IOSXEDriver(
            host=self.ip,
            auth_username=self.username,
            auth_password=self.password,
            auth_secondary=self.enable if self.enable else self.password,
            auth_strict_key=False,
            transport="ssh2",
        )
        self._conn.open()

    def get_device_details(self):
        if self._conn is None:
            self.connect()
        response = self._conn.send_command("show version").genie_parse_output()
        self.platform = response["version"].get("platform")
        self.version = response["version"].get("version")
        self.model = response["version"].get("chassis")
        self.serial = response["version"].get("chassis_sn")
        self.interfaces = response["version"].get("number_of_intfs")
        self.system_image = response["version"].get("system_image")
        response = self._conn.send_command("dir").genie_parse_output()
        self.bytes_free = response["dir"]["flash:/"]["bytes_free"]
