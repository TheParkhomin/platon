from tests.fixtures.wallet import WalletDataGenerator, WalletRepository
from faker import Faker
import pytest


pytestmark = pytest.mark.asyncio


async def test_repo_add(
        wallet_repo: WalletRepository,
        wallet_data_generator: WalletDataGenerator,
        fake: Faker,
):
    user_id = fake.pyint()
    wallet_data = wallet_data_generator.generate_wallet_data(user_id=user_id)
    wallet_raw = await wallet_repo.create(wallet_data['user_id'], wallet_data['address'])
    assert wallet_raw['user_id'] == wallet_data['user_id']
    assert wallet_raw['address'] == wallet_data['address']


async def test_repo_get_by_uid(
        wallet_repo: WalletRepository,
        wallet_data_generator: WalletDataGenerator,
        fake: Faker,
):
    user_id = fake.pyint()
    wallet_data = wallet_data_generator.generate_wallet_data(user_id=user_id)
    wallet = await wallet_repo.create(wallet_data['user_id'], wallet_data['address'])

    wallet_result = await wallet_repo.get_by_uid(wallet['uid'])

    assert wallet_result['uid'] == wallet['uid']
    assert wallet_result['user_id'] == wallet_data['user_id']
    assert wallet_result['address'] == wallet_data['address']
