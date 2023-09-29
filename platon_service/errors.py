class ExpectedError(Exception):
    ...


class ApiExpectedError(Exception):
    ...


class InsufficientFunds(ExpectedError):
    def __init__(self, source_id: int, value: int):
        super().__init__(f"Insufficient funds for wallet {source_id}, amount: {value}")


class WalletNotFount(ExpectedError):
    def __init__(self, wallet_id: int):
        super().__init__(f"Wallet with id {wallet_id} not found")


class WalletAlreadyExists(ExpectedError):
    def __init__(self, user_id: int):
        super().__init__(f"Wallet with user_id {user_id} already exist")


class ApiError(ApiExpectedError):
    def __init__(self, msg: str):
        super().__init__(msg)


class ApiNotFoundError(ApiError):
    ...
