import aiohttp
import pytest
import pytest_asyncio
from aioresponses import aioresponses


@pytest_asyncio.fixture
async def session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture
def mock_server():
    with aioresponses() as m:
        yield m
