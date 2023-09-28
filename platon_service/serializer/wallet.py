from pydantic import BaseModel


class WalletCreateRequest(BaseModel):
    user_id: int


class WalletTransferRequest(BaseModel):
    source_uid: int
    target_uid: int
    value: int


class WalletResponseDetail(BaseModel):
    uid: int
    address: str
    user_id: int
    score: int
