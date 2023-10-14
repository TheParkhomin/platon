from platon_service.api.user import UserApi
from platon_service.api.crypto import JwtApi, CryptoApi
from platon_service.entity.user import UserEntity
from platon_service.entity.authorize import AuthorizeEntity
from platon_service.errors import ApiError


class AuthorizeApi:
    def __init__(self, jwt_api: JwtApi, crypto_api: CryptoApi, user_api: UserApi):
        self._jwt_api = jwt_api
        self._crypto_api = crypto_api
        self._user_api = user_api

    async def sign_up(self, username: str, password: str) -> AuthorizeEntity:
        user: UserEntity = await self._user_api.create(username=username, password=password)
        token = self._jwt_api.encode({'user_id': user.uid})
        return AuthorizeEntity(username=user.username, token=token)

    async def sign_in(self, username: str, password: str) -> AuthorizeEntity:
        user: UserEntity = await self._user_api.get_by_username(username=username)
        check = self._crypto_api.check_hash(secret=user.password, raw=password)
        if not check:
            raise ApiError(msg="Wrong password")
        token = self._jwt_api.encode({'user_id': user.uid})
        return AuthorizeEntity(username=user.username, token=token)
