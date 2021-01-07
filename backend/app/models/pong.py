from pydantic import BaseModel


class Pong(BaseModel):
    ping: str = "pong"
    project: str
    environment: str
