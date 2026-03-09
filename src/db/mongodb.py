from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database():
    return db.client[settings.DATABASE_NAME]


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    # Ping the database to confirm connection
    try:
        await db.client.admin.command("ping")
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")


async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("MongoDB connection closed.")
