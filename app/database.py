from collections.abc import AsyncGenerator

from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.app_debug,
    pool_pre_ping=True,
)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

redis_client: Redis = Redis.from_url(
    settings.redis_url,
    decode_responses=True,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session."""

    async with AsyncSessionLocal() as session:
        yield session


def get_redis_client() -> Redis:
    """Return the shared Redis client."""

    return redis_client


async def check_database_connection() -> bool:
    """Check if the application can connect to PostgreSQL."""

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


async def check_redis_connection() -> bool:
    """Check if the application can connect to Redis."""

    try:
        response = await redis_client.ping()
        return bool(response)
    except Exception:
        return False


async def close_database_connection() -> None:
    """Close the database engine connection pool."""

    await engine.dispose()


async def close_redis_connection() -> None:
    """Close the Redis client connection."""

    await redis_client.aclose()