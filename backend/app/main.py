import uvicorn
from fastapi import FastAPI

from app.api.api import router


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router, prefix="/api")

    return application


app = create_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
