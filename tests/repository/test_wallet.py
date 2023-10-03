from tests.fixtures.wallet import WalletDataGenerator, WalletRepository
from faker import Faker
import pytest
from platon_service.errors import InsufficientFundsError, WalletAlreadyExistsError, WalletNotFoundError


pytestmark = pytest.mark.asyncio


async def test_repo_success_add(
        wallet_repo: WalletRepository,
        wallet_data_generator: WalletDataGenerator,
        fake: Faker,
):
    user_id = fake.pyint()
    wallet_data = wallet_data_generator.generate_args(user_id=user_id)
    wallet_raw = await wallet_repo.create(wallet_data['user_id'], wallet_data['address'])
    assert wallet_raw['user_id'] == wallet_data['user_id']
    assert wallet_raw['address'] == wallet_data['address']


async def test_repo_fail_add(
        wallet_repo: WalletRepository,
        wallet_data_generator: WalletDataGenerator,
        fake: Faker,
):
    user_id = fake.pyint()
    wallet_data = wallet_data_generator.generate_args(user_id=user_id)
    await wallet_repo.create(wallet_data['user_id'], wallet_data['address'])
    try:
        await wallet_repo.create(wallet_data['user_id'], wallet_data['address'])
    except WalletAlreadyExistsError:
        assert True
    else:
        assert False


async def test_repo_get_by_uid(
        wallet_repo: WalletRepository,
        wallet_data_generator: WalletDataGenerator,
        fake: Faker,
):
    user_id = fake.pyint()
    wallet_data = wallet_data_generator.generate_args(user_id=user_id)
    wallet = await wallet_repo.create(wallet_data['user_id'], wallet_data['address'])

    wallet_result = await wallet_repo.get_by_uid(wallet['uid'])

    assert wallet_result['uid'] == wallet['uid']
    assert wallet_result['user_id'] == wallet_data['user_id']
    assert wallet_result['address'] == wallet_data['address']


async def test_repo_get_by_uid_not_found(
        wallet_repo: WalletRepository,
        fake: Faker,
):
    try:
        await wallet_repo.get_by_uid(fake.pyint())
    except WalletNotFoundError:
        assert True
    else:
        assert False


async def test_repo_success_transfer(
        wallet_repo: WalletRepository,
        wallet_data_generator: WalletDataGenerator,
        fake: Faker,
):
    wallet_data_source = wallet_data_generator.generate_args(score=1000)
    wallet_data_target = wallet_data_generator.generate_args()
    wallet_source = await wallet_repo.create(
        user_id=wallet_data_source['user_id'],
        address=wallet_data_source['address'],
        score=wallet_data_source['score'],
    )
    wallet_target = await wallet_repo.create(
        user_id=wallet_data_target['user_id'],
        address=wallet_data_target['address'],
        score=wallet_data_target['score'],
    )

    await wallet_repo.transfer(wallet_source['uid'], wallet_target['uid'], amount=100)

    result_wallet_source = await wallet_repo.get_by_uid(wallet_source['uid'])
    result_wallet_target = await wallet_repo.get_by_uid(wallet_target['uid'])

    assert result_wallet_source['score'] == 900
    assert result_wallet_target['score'] == 100


async def test_repo_fail_transfer(
        wallet_repo: WalletRepository,
        wallet_data_generator: WalletDataGenerator,
        fake: Faker,
):
    wallet_data_source = wallet_data_generator.generate_args(score=100)
    wallet_data_target = wallet_data_generator.generate_args()
    wallet_source = await wallet_repo.create(
        user_id=wallet_data_source['user_id'],
        address=wallet_data_source['address'],
        score=wallet_data_source['score'],
    )
    wallet_target = await wallet_repo.create(
        user_id=wallet_data_target['user_id'],
        address=wallet_data_target['address'],
        score=wallet_data_target['score'],
    )
    try:
        await wallet_repo.transfer(wallet_source['uid'], wallet_target['uid'], amount=150)
    except InsufficientFundsError:
        assert True
    else:
        assert False

    result_wallet_source = await wallet_repo.get_by_uid(wallet_source['uid'])
    result_wallet_target = await wallet_repo.get_by_uid(wallet_target['uid'])

    assert result_wallet_source['score'] == 100
    assert result_wallet_target['score'] == 0
