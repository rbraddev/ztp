from fastapi import APIRouter, Depends

from app.config import get_settings, Settings
from app.models.pong import Pong

router = APIRouter()


@router.get("/ping", response_model=Pong)
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong",
        "project": settings.PROJECT,
        "environment": settings.ENVIRONMENT,
    }
