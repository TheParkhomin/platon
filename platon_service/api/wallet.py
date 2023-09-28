from platon_service.repository.wallet import WalletRepository, WalletRepositoryProtocol
from platon_service.entity.wallet import WalletEntity
import secrets
from platon_service.errors import InsufficientFunds
from typing import Protocol
import abc


class WalletApiProtocol(Protocol):

    @abc.abstractmethod
    async def create(self, user_id: int) -> WalletEntity:
        ...

    @abc.abstractmethod
    async def get_by_uid(self, uid: int) -> WalletEntity | None:
        ...

    @abc.abstractmethod
    async def transfer(self, source_uid: int, target_uid: int, value: int) -> WalletEntity | None:
        ...


class WalletApi:

    def __init__(self, repo: WalletRepositoryProtocol):
        self._repo = repo

    async def create(self, user_id: int) -> WalletEntity:
        address = secrets.token_hex(64)
        wallet_raw = await self._repo.create(user_id, address)
        return WalletEntity(**wallet_raw)

    async def get_by_uid(self, uid: int) -> WalletEntity | None:
        wallet_raw = await self._repo.get_by_uid(uid)
        if not wallet_raw:
            return None

        return WalletEntity(**wallet_raw)

    async def transfer(self, source_uid: int, target_uid: int, value: int) -> WalletEntity | None:
        try:
            await self._repo.transfer(source_uid, target_uid, value)
        except InsufficientFunds:
            return None

        return await self.get_by_uid(source_uid)



