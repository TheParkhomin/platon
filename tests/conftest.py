import pytest
import yoyo
import os
from databases import Database
from faker import Faker
from platon_service.config import PlatonConfig, config_factory
from platon_service.server import Server
from fastapi.testclient import TestClient


@pytest.fixture(scope='session')
def db_instance():
    db_url = os.environ['DB_URL']
    backend = yoyo.get_backend(db_url)
    migrations = yoyo.read_migrations('migrations')
    backend.apply_migrations(backend.to_apply(migrations))
    return Database(db_url, force_rollback=True)


@pytest.fixture
async def connected_db(loop, db_instance: Database):
    async with db_instance:
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
