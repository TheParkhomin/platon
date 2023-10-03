from httpx import Response
from http import HTTPStatus
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from tests.fixtures.wallet import WalletDataGenerator
from tests.mocks.api import WALLET_API
from platon_service.errors import ApiError, ApiNotFoundError
from faker import Faker


async def test_create_view(test_client: TestClient, mocker: MockerFixture, wallet_data_generator: WalletDataGenerator):
    wallet = wallet_data_generator.generate_wallet_entity()
    mock_api = mocker.patch(f'{WALLET_API}.create', return_value=wallet)
    resp: Response = test_client.post('/api/v1/wallet', json={'user_id': wallet.user_id})
    mock_api.assert_awaited()
    assert resp.status_code == HTTPStatus.OK
    result = resp.json()
    assert result['uid'] == wallet.uid
    assert result['user_id'] == wallet.user_id
    assert result['address'] == wallet.address
    assert result['score'] == wallet.score


async def test_create_view_fail(
        test_client: TestClient, mocker: MockerFixture, wallet_data_generator: WalletDataGenerator, fake: Faker,
):
    mock_api = mocker.patch(f'{WALLET_API}.create', side_effect=ApiError('error'))
    resp: Response = test_client.post('/api/v1/wallet', json={'user_id': fake.pyint()})
    mock_api.assert_awaited()
    assert resp.status_code == HTTPStatus.BAD_REQUEST


async def test_get_view(test_client: TestClient, mocker: MockerFixture, wallet_data_generator: WalletDataGenerator):
    wallet = wallet_data_generator.generate_wallet_entity()
    mock_api = mocker.patch(f'{WALLET_API}.get_by_uid', return_value=wallet)
    resp: Response = test_client.get(f'/api/v1/wallet/{wallet.uid}/')
    mock_api.assert_awaited()
    assert resp.status_code == HTTPStatus.OK
    result = resp.json()
    assert result['uid'] == wallet.uid
    assert result['user_id'] == wallet.user_id
    assert result['address'] == wallet.address
    assert result['score'] == wallet.score


async def test_get_view_fail(
        test_client: TestClient, mocker: MockerFixture, wallet_data_generator: WalletDataGenerator,
):

    mocker_api = mocker.patch(f'{WALLET_API}.get_by_uid', side_effect=ApiNotFoundError('error'))
    resp: Response = test_client.get(f'/api/v1/wallet/1/')
    mocker_api.assert_awaited()
    assert resp.status_code == HTTPStatus.NOT_FOUND
