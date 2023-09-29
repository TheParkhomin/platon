from http import HTTPStatus

from fastapi.responses import JSONResponse

from platon_service.api.wallet import WalletApiProtocol
from platon_service.entity.wallet import WalletEntity
from platon_service.errors import ApiError, ApiNotFoundError
from platon_service.serializer.wallet import (
    WalletCreateRequest,
    WalletResponseDetail,
    WalletTransferRequest,
)


class WalletView:
    def __init__(self, api: WalletApiProtocol):
        self._api = api

    async def create(self, request: WalletCreateRequest):
        try:
            wallet: WalletEntity = await self._api.create(**dict(request))
        except ApiError as err:
            return JSONResponse(status_code=400, content={"message": str(err)})

        return WalletResponseDetail(**dict(wallet))

    async def get_by_uid(self, uid: int):
        try:
            wallet: WalletEntity = await self._api.get_by_uid(uid)
        except ApiNotFoundError as err:
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND, content={"message": str(err)}
            )
        return WalletResponseDetail(**dict(wallet))

    async def transfer(self, request: WalletTransferRequest):
        try:
            wallet: WalletEntity = await self._api.transfer(**dict(request))
        except ApiError as err:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST, content={"message": str(err)}
            )

        return WalletEntity(**dict(wallet))
