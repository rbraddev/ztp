from ruamel.yaml import YAML


class Config:
    def __init__(self):
        yaml = YAML(typ="safe")
        with open("config.yaml", "r") as f:
            config = yaml.load(f.read())

        self.swversions: dict = config.get("swversions")
        self.credentials: dict = config.get("credentials")
