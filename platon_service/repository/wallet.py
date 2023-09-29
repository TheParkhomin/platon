import abc
from typing import Mapping, Protocol, cast

from asyncpg.exceptions import CheckViolationError, UniqueViolationError
from databases import Database

from platon_service.errors import InsufficientFunds, WalletAlreadyExists, WalletNotFount


class WalletRepositoryProtocol(Protocol):
    @abc.abstractmethod
    async def create(self, user_id: int, address: str) -> Mapping:
        ...

    @abc.abstractmethod
    async def get_by_uid(self, uid: int) -> Mapping:
        ...

    @abc.abstractmethod
    async def transfer(self, source_uid: int, target_uid: int, value: int) -> None:
        ...


class WalletRepository:
    def __init__(self, db: Database):
        self._db = db

    async def get_by_uid(self, uid: int) -> Mapping:
        query = """
            SELECT uid, address, user_id, score FROM wallets WHERE uid = :uid
        """
        values = {"uid": uid}

        row = await self._db.fetch_one(query, values)
        if not row:
            raise WalletNotFount(wallet_id=uid)
        return cast(Mapping, row)

    async def create(self, user_id: int, address: str) -> Mapping:
        query = """
            INSERT INTO wallets (user_id, address, score) VALUES
            (:user_id, :address, 0)
            
            RETURNING uid, user_id, address, score
        """
        values = {"user_id": user_id, "address": address}
        try:
            row = await self._db.fetch_one(query, values)
        except UniqueViolationError:
            raise WalletAlreadyExists(user_id)

        return cast(Mapping, row)

    async def transfer(self, source_uid: int, target_uid: int, value: int) -> None:
        try:
            async with self._db.transaction():
                await self._db.execute(
                    "SELECT * FROM wallets WHERE uid in (:source_uid, :target_uid) FOR UPDATE;",
                    {"source_uid": source_uid, "target_uid": target_uid},
                )
                await self._db.execute(
                    "UPDATE wallets SET score = score - :transfer WHERE uid = :source_uid;",
                    {"source_uid": source_uid, "transfer": value},
                )
                await self._db.execute(
                    "UPDATE wallets SET score = score + :transfer WHERE uid = :target_uid;",
                    {"target_uid": target_uid, "transfer": value},
                )
        except CheckViolationError:
            raise InsufficientFunds(source_id=source_uid, value=value)
