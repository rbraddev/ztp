from pydantic import BaseModel


class DeviceVersion(BaseModel):
    version: str
    image: str
