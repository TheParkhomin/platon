from platon_service.repository.wallet import WalletRepository
import pytest
from tests.fixtures.base import BaseDataGenerator
import secrets


class WalletDataGenerator(BaseDataGenerator):
    def generate_wallet_data(self, **kwargs):
        return {
            'user_id': self._fake.pyint(),
            'address': secrets.token_hex(),
            'score': 0,
        } | kwargs


@pytest.fixture
def wallet_repo(connected_db):
    return WalletRepository(db=connected_db)


@pytest.fixture
def wallet_data_generator(fake):
    return WalletDataGenerator(fake)

