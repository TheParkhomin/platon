from pydantic import BaseModel


class WalletEntity(BaseModel):
    uid: int
    address: str
    user_id: int
    score: int
