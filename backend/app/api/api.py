from fastapi import APIRouter

from app.api.endpoints import ping, provisioning

router = APIRouter()
router.include_router(ping.router)
router.include_router(provisioning.router, prefix="/provisioning")
