import abc
from typing import Mapping, Protocol, cast

from asyncpg.exceptions import CheckViolationError, UniqueViolationError
from databases import Database

from platon_service.errors import (
    InsufficientFundsError,
    WalletAlreadyExistsError,
    WalletNotFoundError,
)


class WalletRepositoryProtocol(Protocol):
    @abc.abstractmethod
    async def create(self, user_id: int, address: str) -> Mapping:
        ...  # noqa: WPS428

    @abc.abstractmethod
    async def get_by_uid(self, uid: int) -> Mapping:
        ...  # noqa: WPS428

    @abc.abstractmethod
    async def transfer(self, source_uid: int, target_uid: int, amount: int) -> None:
        ...  # noqa: WPS428


class WalletRepository:
    def __init__(self, db: Database):
        self._db = db

    async def get_by_uid(self, uid: int) -> Mapping:
        query = """
            SELECT uid, address, user_id, score FROM wallets WHERE uid = :uid
        """
        query_values = {"uid": uid}

        row = await self._db.fetch_one(query, query_values)
        if not row:
            raise WalletNotFoundError(wallet_id=uid)
        return cast(Mapping, row)

    async def create(self, user_id: int, address: str) -> Mapping:
        query = """
            INSERT INTO wallets (user_id, address, score) VALUES
            (:user_id, :address, 0)            
            RETURNING uid, user_id, address, score
        """
        query_values = {"user_id": user_id, "address": address}
        try:
            row = await self._db.fetch_one(query, query_values)
        except UniqueViolationError as err:
            raise WalletAlreadyExistsError(user_id) from err

        return cast(Mapping, row)

    async def transfer(self, source_uid: int, target_uid: int, amount: int) -> None:
        try:
            async with self._db.transaction():
                await self._db.execute(
                    "SELECT * FROM wallets WHERE uid in (:source_uid, :target_uid) FOR UPDATE;",
                    {"source_uid": source_uid, "target_uid": target_uid},
                )
                await self._db.execute(
                    "UPDATE wallets SET score = score - :transfer WHERE uid = :source_uid;",
                    {"source_uid": source_uid, "transfer": amount},
                )
                await self._db.execute(
                    "UPDATE wallets SET score = score + :transfer WHERE uid = :target_uid;",
                    {"target_uid": target_uid, "transfer": amount},
                )
        except CheckViolationError as err:
            raise InsufficientFundsError(source_id=source_uid, amount=amount) from err
