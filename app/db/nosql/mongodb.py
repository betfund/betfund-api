"""Establish Motor Connection."""

from motor.motor_asyncio import AsyncIOMotorClient
from app.db.nosql.init_db import nsqldb


async def get_database() -> AsyncIOMotorClient:
    """Build Async Database Client."""
    return nsqldb.client
