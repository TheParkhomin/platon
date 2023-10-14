from pydantic import BaseModel


class AuthorizeEntity(BaseModel):
    username: str
    token: str
