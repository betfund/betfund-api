import os

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.nosql.init_db import nsqldb

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def create_mongo_client():
    """Initiate AsyncIOMotorClient."""
    nsqldb.client = AsyncIOMotorClient(
        settings.MONGO_CONNECTION
    )


async def shutdown_mongo_client():
    """Close AsyncIOMotorClient."""
    nsqldb.client.close()

app.add_event_handler("startup", create_mongo_client)
app.add_event_handler("shutdown", shutdown_mongo_client)


app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
