import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from beanie import init_beanie
from app.models.user_model import User
from app.models.linkedin_model import LinkedinConnect
from app.models.post_model import Post

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongo():
    global client, db
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB]
        await init_beanie(database=client[settings.MONGO_DB], document_models=[User,LinkedinConnect,Post])
        # Test the connection
        await client.admin.command("ping")
        logger.info("✅ Successfully connected to MongoDB: %s", settings.MONGO_DB)
    except Exception as e:
        logger.error("❌ Failed to connect to MongoDB: %s", str(e))
        raise e


async def close_mongo_connection():
    global client
    if client:
        await client.close()
        logger.info("🔌 MongoDB connection closed")
