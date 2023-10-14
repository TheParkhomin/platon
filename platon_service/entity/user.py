from pydantic import BaseModel


class UserEntity(BaseModel):
    uid: int
    username: str
    password: str
