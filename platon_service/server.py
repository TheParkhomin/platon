from fastapi import FastAPI, APIRouter
from platon_service.view.ping import ping


class Server:
    def __init__(self):
        self._router = APIRouter()
        self._app = FastAPI()
        self._create_routes()

        self._app.include_router(self._router)

    def _create_routes(self):
        self._router.add_api_route('/ping', endpoint=ping, methods=['GET'])

    def get_app(self):
        return self._app
