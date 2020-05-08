from typing import Any

from fastapi import APIRouter, Depends

from app.db.nosql import mongodb
from app.db.nosql.upcoming_events import get_upcoming_events

from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()


@router.get("/upcoming")
async def fetch_events(
    as_of: str = "",
    sport_id: str = "",
    limit: int = 500,
    offset: int = 0,
    db: AsyncIOMotorClient = Depends(mongodb.get_database)
) -> Any:
    """
    Retrieve Upcoming Events.
    """
    events = await get_upcoming_events(
        conn=db,
        as_of=as_of,
        sport_id=sport_id,
        limit=limit,
        offset=offset
    )

    return {
        "upcomingEvents": events
    }
