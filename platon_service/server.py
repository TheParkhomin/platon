from databases import Database
from fastapi import APIRouter, FastAPI

from platon_service.api.authorize import AuthorizeApi
from platon_service.api.wallet import WalletApi
from platon_service.api.user import UserApi
from platon_service.api.crypto import JwtApi, CryptoApi
from platon_service.config import config_factory, PlatonConfig
from platon_service.repository.wallet import WalletRepository
from platon_service.repository.user import UserRepository
from platon_service.serializer.wallet import WalletResponseDetail
from platon_service.serializer.authorize import AuthorizeResponse
from platon_service.view.ping import PingView
from platon_service.view.wallet import WalletView
from platon_service.view.authorize import SignUpView, SignInView


class Server:
    def __init__(self):
        self._router = APIRouter(prefix="/api/v1")
        self._app = FastAPI()

        platon_config: PlatonConfig = config_factory()

        self._db = Database(platon_config.database.url)
        self._wallet_repo = WalletRepository(db=self._db)
        self._user_repo = UserRepository(db=self._db)
        self._wallet_api = WalletApi(repo=self._wallet_repo)
        self._crypto_api = CryptoApi(salt=platon_config.hash_salt)
        self._jwt_api = JwtApi(secret=platon_config.jwt_secret)
        self._user_api = UserApi(repo=self._user_repo, crypto_api=self._crypto_api)
        self._auth_api = AuthorizeApi(jwt_api=self._jwt_api, crypto_api=self._crypto_api, user_api=self._user_api)

        self._app.add_event_handler("shutdown", self._db.disconnect)
        self._app.add_event_handler("startup", self._db.connect)
        self._create_routes()

    @property
    def app(self):
        return self._app

    def _create_routes(self):
        wallet_view = WalletView(api=self._wallet_api)
        sign_up_view = SignUpView(api=self._auth_api)
        sign_in_view = SignInView(api=self._auth_api)
        self._router.add_api_route(
            "/ping",
            endpoint=PingView(wallet_repo=self._wallet_repo).ping,
            methods=["GET"],
        )
        self._router.add_api_route(
            "/wallet/{uid}",
            endpoint=wallet_view.get_by_uid,
            methods=["GET"],
            response_model=WalletResponseDetail,
        )
        self._router.add_api_route(
            "/wallet",
            endpoint=wallet_view.create,
            methods=["POST"],
            response_model=WalletResponseDetail,
        )
        self._router.add_api_route(
            "/wallet/transfer",
            endpoint=wallet_view.transfer,
            methods=["POST"],
            response_model=WalletResponseDetail,
        )
        self._router.add_api_route(
            "/auth/signup",
            endpoint=sign_up_view.post,
            methods=["POST"],
            response_model=AuthorizeResponse,
        ),
        self._router.add_api_route(
            "/auth/signin",
            endpoint=sign_in_view.post,
            methods=["POST"],
            response_model=AuthorizeResponse,
        ),
        self._app.include_router(self._router)
