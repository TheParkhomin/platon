from platon_service.api.authorize import AuthorizeApi
from platon_service.serializer.authorize import AuthorizeRequest, AuthorizeResponse
from platon_service.errors import ApiError
from fastapi.responses import JSONResponse
from http import HTTPStatus


class BaseAuth:
    def __init__(self, api: AuthorizeApi):
        self._api = api

    async def post(self, request: AuthorizeRequest):
        try:
            response: AuthorizeResponse = await self._action(request)
        except ApiError as err:
            return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"message": str(err)})
        return response

    async def _action(self, request: AuthorizeRequest):
        raise NotImplemented()


class SignUpView(BaseAuth):
    async def _action(self, request: AuthorizeRequest):
        user = await self._api.sign_up(username=request.username, password=request.password)
        return AuthorizeResponse(**dict(user))


class SignInView(BaseAuth):
    async def _action(self, request: AuthorizeRequest):
        user = await self._api.sign_in(username=request.username, password=request.password)
        return AuthorizeResponse(**dict(user))
