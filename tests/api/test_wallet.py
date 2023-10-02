from pytest_mock import MockerFixture
from tests.mocks.repository import WALLET_REPOSITORY


async def test_create_wallet(mocker: MockerFixture):
    mocker.patch(f'{WALLET_REPOSITORY}.create', return_value={})

