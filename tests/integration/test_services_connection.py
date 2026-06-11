import os

import pytest

from app.database import check_database_connection, check_redis_connection

pytestmark = pytest.mark.skipif(
    os.getenv("ODDS_ENGINE_RUN_INTEGRATION_TESTS") != "1",
    reason="Integration tests require running PostgreSQL and Redis services.",
)


@pytest.mark.asyncio
async def test_database_connection_is_available() -> None:
    assert await check_database_connection() is True


@pytest.mark.asyncio
async def test_redis_connection_is_available() -> None:
    assert await check_redis_connection() is True