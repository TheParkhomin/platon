from platon_service.repository.wallet import WalletRepository
import pytest
from tests.fixtures.base import BaseDataGenerator
import secrets
from platon_service.api.wallet import WalletApi
from platon_service.entity.wallet import WalletEntity
from typing import Mapping


class WalletDataGenerator(BaseDataGenerator):
    def generate_args(self, **kwargs) -> Mapping:
        return {
            'user_id': self._fake.pyint(),
            'address': secrets.token_hex(),
            'score': 0,
        } | kwargs

    def generate_wallet_data(self, **kwargs) -> Mapping:
        return {
            'uid': self._fake.pyint(),
            'user_id': self._fake.pyint(),
            'address': secrets.token_hex(),
            'score': 0,
        } | kwargs

    def generate_wallet_entity(self, **kwargs) -> WalletEntity:
        wallet_data = self.generate_wallet_data(**kwargs)
        return WalletEntity(**wallet_data)


@pytest.fixture
def wallet_repo(connected_db):
    return WalletRepository(db=connected_db)


@pytest.fixture
def wallet_data_generator(fake):
    return WalletDataGenerator(fake)


@pytest.fixture
def wallet_api(wallet_repo):
    return WalletApi(repo=wallet_repo)
