from core.utils import load_yaml


class Config:
    def __init__(self):
        config = load_yaml("config.yaml")

        self.swversions: dict = config.get("swversions")
        self.credentials: dict = config.get("credentials")
