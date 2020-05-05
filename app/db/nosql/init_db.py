"""Create database instance with Motor Client."""
from motor.motor_asyncio import AsyncIOMotorClient


class Database(object):
    """Mongo Database Placeholder."""
    client: AsyncIOMotorClient = None


nsqldb = Database()
