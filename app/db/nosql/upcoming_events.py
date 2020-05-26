"""Query operations for upcomingEvents collection."""
from app.db.nosql.init_db import AsyncIOMotorClient
from app.core.config import settings


async def get_upcoming_events(
    conn: AsyncIOMotorClient,
    as_of: int,
    sport_id: str,
    limit: int = 500,
    offset: int = 0
):
    """
    Retrieves events in upcomingEvents collection.
    Args:
        conn (AsyncIOMotorClient): MongoDB connection
        as_of (str): Epoch timestamp floor for events to fetch
        sport_id (str): Internal id for sport to fetch
        limit (int): Length limit of result set
        offset (int): Starting point of result set
    Returns:
        list: Array of documents from upcomingEvents collection
    """
    database = settings.MONGO_DATABASE
    collection = settings.MONGO_EVENTS_COLLECTION

    filter = {
            "data.time": {
                "$gt": as_of  # greater than operator
            },
            "data.sport_id": sport_id,
        }

    if not sport_id:
        del filter["data.sport_id"]

    # Establish collection connection and query
    cursor = conn[database][collection].find(
        filter=filter,
        limit=limit,
        skip=offset
    )

    upcoming_events_docs = []
    cursor.sort('data.updated_at', -1).skip(1)  # ensure cursor stats at value
    async for document in cursor:
        upcoming_events_docs.append(document)

    return upcoming_events_docs
