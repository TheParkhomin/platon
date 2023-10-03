from pytest_mock import MockerFixture
from tests.mocks.repository import WALLET_REPOSITORY
from tests.fixtures.wallet import WalletDataGenerator, WalletApi
from faker import Faker
from platon_service.errors import (
    WalletAlreadyExistsError,
    ApiError,
    WalletNotFoundError,
    InsufficientFundsError,
    ApiNotFoundError,
)


async def test_create_wallet(
        mocker: MockerFixture,
        wallet_data_generator: WalletDataGenerator,
        wallet_api: WalletApi,
        fake: Faker,
):
    user_id = fake.pyint()
    wallet_data = wallet_data_generator.generate_wallet_data(user_id=user_id)
    mock_repo = mocker.patch(f'{WALLET_REPOSITORY}.create', return_value=wallet_data)
    wallet = await wallet_api.create(user_id)
    mock_repo.assert_awaited()
    assert wallet.uid == wallet_data['uid']
    assert wallet.user_id == wallet_data['user_id']
    assert wallet.address == wallet_data['address']
    assert wallet.score == wallet_data['score']


async def test_create_fail_wallet(
        mocker: MockerFixture,
        wallet_data_generator: WalletDataGenerator,
        wallet_api: WalletApi,
        fake: Faker,
):
    user_id = fake.pyint()
    mock_repo = mocker.patch(f'{WALLET_REPOSITORY}.create', side_effect=WalletAlreadyExistsError(user_id=user_id))
    try:
        await wallet_api.create(user_id)
    except ApiError:
        assert True
    else:
        assert False
    mock_repo.assert_awaited()


async def test_get_wallet_by_uid(
        mocker: MockerFixture,
        wallet_data_generator: WalletDataGenerator,
        wallet_api: WalletApi,
        fake: Faker,
):
    wallet_data = wallet_data_generator.generate_wallet_data()
    mock_repo = mocker.patch(f'{WALLET_REPOSITORY}.get_by_uid', return_value=wallet_data)
    wallet = await wallet_api.get_by_uid(wallet_data['uid'])
    mock_repo.assert_awaited()
    assert wallet.uid == wallet_data['uid']
    assert wallet.user_id == wallet_data['user_id']
    assert wallet.address == wallet_data['address']
    assert wallet.score == wallet_data['score']


async def test_get_fail_wallet(
        mocker: MockerFixture,
        wallet_data_generator: WalletDataGenerator,
        wallet_api: WalletApi,
        fake: Faker,
):
    wallet_uid = fake.pyint()
    mock_repo = mocker.patch(f'{WALLET_REPOSITORY}.get_by_uid', side_effect=WalletNotFoundError(wallet_id=wallet_uid))
    try:
        await wallet_api.get_by_uid(wallet_uid)
    except ApiNotFoundError:
        assert True
    else:
        assert False
    mock_repo.assert_awaited()


async def test_transfer_success(
        mocker: MockerFixture,
        wallet_data_generator: WalletDataGenerator,
        wallet_api: WalletApi,
        fake: Faker,
):
    wallet_data = wallet_data_generator.generate_wallet_data()
    mock_repo_get = mocker.patch(f'{WALLET_REPOSITORY}.get_by_uid', return_value=wallet_data)
    mock_repo_transfer = mocker.patch(f'{WALLET_REPOSITORY}.transfer', return_value=None)
    await wallet_api.transfer(source_uid=fake.pyint(), target_uid=fake.pyint(), amount=fake.pyint())
    mock_repo_transfer.assert_awaited()
    mock_repo_get.assert_awaited()


async def test_transfer_fail(
        mocker: MockerFixture,
        wallet_data_generator: WalletDataGenerator,
        wallet_api: WalletApi,
        fake: Faker,
):
    mock_repo_transfer = mocker.patch(
        f'{WALLET_REPOSITORY}.transfer', side_effe=InsufficientFundsError(source_id=fake.pyint(), amount=0),
    )
    try:
        await wallet_api.transfer(source_uid=fake.pyint(), target_uid=fake.pyint(), amount=fake.pyint())
    except ApiError:
        assert True
    else:
        assert False
    mock_repo_transfer.assert_awaited()
