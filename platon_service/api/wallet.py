import abc
import secrets
from typing import Protocol

from platon_service.entity.wallet import WalletEntity
from platon_service.errors import (
    ApiError,
    ApiNotFoundError,
    InsufficientFundsError,
    WalletAlreadyExistsError,
    WalletNotFoundError,
)
from platon_service.repository.wallet import WalletRepositoryProtocol


class WalletApiProtocol(Protocol):
    """Api class for working with wallets."""

    @abc.abstractmethod
    async def create(self, user_id: int) -> WalletEntity:
        """Create wallet for user id.

        Args:
            user_id: user id for create wallet;

        Returns:
            WalletEntity: new wallet;
        """

    @abc.abstractmethod
    async def get_by_uid(self, uid: int) -> WalletEntity:
        """Get wallet entity by wallet uid.

        Args:
            uid: the wallet uid;

        Returns:
            WalletEntity: wallet with source uid;
        """

    @abc.abstractmethod
    async def transfer(
        self, source_uid: int, target_uid: int, amount: int,
    ) -> WalletEntity:
        """Transfer money from source wallet to target wallet.

        Args:
            source_uid: The source uid;
            target_uid: The target uid;
            amount: the amount to transfer;

        Returns:
            WalletEntity: sources wallet
        """


class WalletApi:
    _size_of_hash = 64

    def __init__(self, repo: WalletRepositoryProtocol):
        self._repo = repo

    async def create(self, user_id: int) -> WalletEntity:
        address = secrets.token_hex(self._size_of_hash)
        try:
            wallet_raw = await self._repo.create(user_id, address)
        except WalletAlreadyExistsError as err:
            raise ApiError(msg=str(err)) from err

        return WalletEntity(**wallet_raw)

    async def get_by_uid(self, uid: int) -> WalletEntity:

        try:
            wallet_raw = await self._repo.get_by_uid(uid)
        except WalletNotFoundError as err:
            raise ApiNotFoundError(str(err)) from err

        return WalletEntity(**wallet_raw)

    async def transfer(self, source_uid: int, target_uid: int, amount: int) -> WalletEntity:
        try:
            await self._repo.transfer(source_uid, target_uid, amount)
        except InsufficientFundsError as err:
            raise ApiError(msg=str(err)) from err

        return await self.get_by_uid(source_uid)
