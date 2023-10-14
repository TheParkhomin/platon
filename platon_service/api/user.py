from platon_service.repository.user import UserRepository
from platon_service.api.crypto import CryptoApi
from platon_service.entity.user import UserEntity
from platon_service.errors import UserAlreadyExist, ApiError, UsernameNotFoundError


class UserApi:
    def __init__(self, repo: UserRepository, crypto_api: CryptoApi):
        self._repo = repo
        self._crypto_api = crypto_api

    async def create(self, username: str, password: str) -> UserEntity:
        password_hash = self._crypto_api.create_hash(password)

        try:
            user_raw = await self._repo.create(username=username, password_hash=password_hash)
        except UserAlreadyExist as err:
            raise ApiError(msg=str(err)) from err

        return UserEntity(**user_raw)

    async def get_by_username(self, username: str) -> UserEntity:
        try:
            user_raw = await self._repo.get_by_username(username)
        except UsernameNotFoundError as err:
            raise ApiError(msg=str(err)) from err

        return UserEntity(**user_raw)
