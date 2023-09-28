from platon_service.api.wallet import WalletApi, WalletApiProtocol
from platon_service.entity.wallet import WalletEntity
from platon_service.serializer.wallet import WalletResponseDetail, WalletCreateRequest, WalletTransferRequest
from typing import Optional, Union
from fastapi.responses import JSONResponse, Response


class WalletView:

    def __init__(self, api: WalletApiProtocol):
        self._api = api

    async def create(self, request: WalletCreateRequest):
        wallet: WalletEntity = await self._api.create(**dict(request))
        return WalletResponseDetail(**dict(wallet))

    async def get_by_uid(self, uid: int):
        wallet: WalletEntity = await self._api.get_by_uid(uid)
        if not wallet:
            return Response(status_code=404)

        return WalletResponseDetail(**dict(wallet))

    async def transfer(self, request: WalletTransferRequest):
        wallet = await self._api.transfer(**dict(request))
        if not wallet:
            return JSONResponse(status_code=400, content={'message': 'Not money'})

        return WalletEntity(**dict(wallet))
