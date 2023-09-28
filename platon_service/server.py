from fastapi import FastAPI, APIRouter
from platon_service.view.ping import PingView
from databases import Database
from platon_service.config import config_factory
from platon_service.repository.wallet import WalletRepository
from platon_service.api.wallet import WalletApi
from platon_service.view.wallet import WalletView
from platon_service.serializer.wallet import WalletResponseDetail


class Server:
    def __init__(self):
        self._router = APIRouter(prefix='/api/v1')
        self._app = FastAPI()

        platon_config = config_factory()

        self._db = Database(platon_config.database.url)
        self._wallet_repo = WalletRepository(db=self._db)
        self._wallet_api = WalletApi(repo=self._wallet_repo)

        self._app.add_event_handler('shutdown', self._db.disconnect)
        self._app.add_event_handler('startup', self._db.connect)
        self._create_routes()

    def _create_routes(self):
        wallet_view = WalletView(api=self._wallet_api)
        self._router.add_api_route(
            '/ping', endpoint=PingView(wallet_repo=self._wallet_repo).ping, methods=['GET'],
        )
        self._router.add_api_route(
            '/wallet/{uid}', endpoint=wallet_view.get_by_uid, methods=['GET'], response_model=WalletResponseDetail,
        )
        self._router.add_api_route(
            '/wallet', endpoint=wallet_view.create, methods=['POST'], response_model=WalletResponseDetail,
        ),
        self._router.add_api_route(
            '/wallet/transfer', endpoint=wallet_view.transfer, methods=['POST'], response_model=WalletResponseDetail,
        )
        self._app.include_router(self._router)

    def get_app(self):
        return self._app
