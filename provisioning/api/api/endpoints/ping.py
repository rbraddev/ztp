from fastapi import APIRouter, Depends

from config import get_settings, Settings
from models.pong import Pong

router = APIRouter()


@router.get("/ping", response_model=Pong)
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong",
        "project": settings.PROJECT,
    }
