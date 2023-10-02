import pytest
import yoyo
import os
from databases import Database
from faker import Faker
from platon_service.config import PlatonConfig, config_factory
from platon_service.server import Server
from fastapi.testclient import TestClient
import asyncio


pytest_plugins = (
    "tests.fixtures.wallet",
    "pytest_asyncio"
)


# @pytest.fixture(scope="session")
# def loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#

@pytest.fixture
async def db_instance():
    db_url = os.environ['DB_URL']
    backend = yoyo.get_backend(db_url)
    migrations = yoyo.read_migrations('migrations')
    backend.apply_migrations(backend.to_apply(migrations))
    return Database(db_url, force_rollback=True)


@pytest.fixture
async def connected_db(db_instance: Database):
    await db_instance.connect()
    yield db_instance


@pytest.fixture
def fake() -> Faker:
    return Faker()


@pytest.fixture(scope='session')
def conf() -> PlatonConfig:
    return config_factory()


@pytest.fixture
def server() -> Server:
    return Server()


@pytest.fixture
def test_client(server):
    client = TestClient(server.app)
    return client
