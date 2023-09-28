from platon_service.serializer.ping import PingResponse
from databases import Database


class PingView:
    def __init__(self, db:Database):
        self._db = db

    async def ping(self) -> PingResponse:
        return PingResponse(message='OK')
