import aiohttp
import pytest_asyncio
from aiointercept import aiointercept


@pytest_asyncio.fixture
async def session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest_asyncio.fixture
async def mock_server():
    async with aiointercept(mock_external_urls=True) as m:
        yield m
