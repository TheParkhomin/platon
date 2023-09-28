from fastapi import FastAPI, APIRouter
from platon_service.view.ping import PingView
from databases import Database
from platon_service.config import config_factory


class Server:
    def __init__(self):
        self._router = APIRouter(prefix='/api/v1')
        self._app = FastAPI()

        platon_config = config_factory()

        self._db = Database(platon_config.database.url)
        self._app.add_event_handler('shutdown', self._db.disconnect)
        self._create_routes()

    def _create_routes(self):
        self._router.add_api_route('/ping', endpoint=PingView(db=self._db).ping, methods=['GET'])
        self._app.include_router(self._router)

    def get_app(self):
        return self._app
