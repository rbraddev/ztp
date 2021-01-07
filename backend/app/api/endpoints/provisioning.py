from fastapi import APIRouter, Depends, HTTPException

from app.config import get_settings, Settings
from app.models.provisioning import DeviceVersion

router = APIRouter()


@router.get("/version/{device}", response_model=DeviceVersion)
async def device_version(device: str, settings: Settings = Depends(get_settings)):
    version_info = settings.SWVERSIONS.get(device)
    if version_info is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return version_info
