from databases import Database
from typing import Mapping, cast
from asyncpg.exceptions import UniqueViolationError
from platon_service.errors import UserAlreadyExist, UsernameNotFoundError


class UserRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def create(self, username: str, password_hash: str) -> Mapping:
        query = """
        INSERT INTO users(username, password) VALUES
        (:username, :password)
        
        RETURNING uid, username, password
        """

        query_values = {'username': username, 'password': password_hash}

        try:
            raw = await self._db.fetch_one(query, query_values)
        except UniqueViolationError as err:
            raise UserAlreadyExist(username) from err

        return cast(Mapping, raw)

    async def get_by_username(self, username: str) -> Mapping:
        query = """
        SELECT uid, username, password FROM users WHERE username = :username
        """

        query_values = {"username": username}

        raw = await self._db.fetch_one(query, query_values)
        if not raw:
            raise UsernameNotFoundError(username)

        return cast(Mapping, raw)
