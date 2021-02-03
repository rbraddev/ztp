import logging
from functools import lru_cache

from pydantic import BaseSettings
from ruamel.yaml import YAML

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    PROJECT: str = None
    ENVIRONMENT: str = None
    SWVERSIONS: dict = None


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")

    yaml = YAML(typ="safe")
    with open("config.yaml", "r") as f:
        settings = yaml.load(f.read())

    return Settings(
        PROJECT=settings.get("project"), SWVERSIONS=settings.get("swversions")
    )
