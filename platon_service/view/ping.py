from platon_service.serializer.ping import PingResponse


class PingView:
    def __init__(self, wallet_repo):
        self.wallet_repo = wallet_repo

    async def ping(self) -> PingResponse:
        return PingResponse(message="OK")
