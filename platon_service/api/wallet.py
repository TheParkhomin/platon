from platon_service.repository.wallet import WalletRepository, WalletRepositoryProtocol
from platon_service.entity.wallet import WalletEntity
import secrets
from platon_service.errors import InsufficientFunds, WalletAlreadyExists, ApiError, WalletNotFount, ApiNotFoundError
from typing import Protocol
import abc


class WalletApiProtocol(Protocol):

    @abc.abstractmethod
    async def create(self, user_id: int) -> WalletEntity:
        ...

    @abc.abstractmethod
    async def get_by_uid(self, uid: int) -> WalletEntity:
        ...

    @abc.abstractmethod
    async def transfer(self, source_uid: int, target_uid: int, value: int) -> WalletEntity:
        ...


class WalletApi:
    _SIZE_OF_HASH = 64

    def __init__(self, repo: WalletRepositoryProtocol):
        self._repo = repo

    async def create(self, user_id: int) -> WalletEntity:

        address = secrets.token_hex(self._SIZE_OF_HASH)
        try:
            wallet_raw = await self._repo.create(user_id, address)
        except WalletAlreadyExists as err:
            raise ApiError(msg=str(err))

        return WalletEntity(**wallet_raw)

    async def get_by_uid(self, uid: int) -> WalletEntity:
        try:
            wallet_raw = await self._repo.get_by_uid(uid)
        except WalletNotFount as err:
            raise ApiNotFoundError(str(err))

        return WalletEntity(**wallet_raw)

    async def transfer(self, source_uid: int, target_uid: int, value: int) -> WalletEntity:
        try:
            await self._repo.transfer(source_uid, target_uid, value)
        except InsufficientFunds as err:
            raise ApiError(msg=str(err))

        return await self.get_by_uid(source_uid)
