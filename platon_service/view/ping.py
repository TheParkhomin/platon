from platon_service.serializer.ping import PingResponse


async def ping() -> PingResponse:
    return PingResponse(message='OK')
