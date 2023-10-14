from pydantic import BaseModel


class AuthorizeRequest(BaseModel):
    username: str
    password: str


class AuthorizeResponse(BaseModel):
    username: str
    token: str
