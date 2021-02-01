# from scrapli import Scrapli


class Host:
    def __init__(self, ip: str, username: str, password: str):
        self.ip = ip
        self.username = username
        self.password = password

        self.driver = None
