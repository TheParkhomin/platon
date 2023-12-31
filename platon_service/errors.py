class ExpectedError(Exception):
    ...


class ApiExpectedError(Exception):
    ...


class InsufficientFundsError(ExpectedError):
    def __init__(self, source_id: int, amount: int):
        super().__init__(f"Insufficient funds for wallet {source_id}, amount: {amount}")


class WalletNotFoundError(ExpectedError):
    def __init__(self, wallet_id: int):
        super().__init__(f"Wallet with id {wallet_id} not found")


class UserNotFoundError(ExpectedError):
    def __init__(self, user_id: int):
        super().__init__(f"User with id {user_id} not found")


class UsernameNotFoundError(ExpectedError):
    def __init__(self, username: str):
        super().__init__(f"User with username {username} not found")


class WalletAlreadyExistsError(ExpectedError):
    def __init__(self, user_id: int):
        super().__init__(f"Wallet with user_id {user_id} already exist")


class UserAlreadyExist(ExpectedError):

    def __init__(self, username: str):
        super().__init__(f"User with username {username} already exist")


class ApiError(ApiExpectedError):
    def __init__(self, msg: str):
        super().__init__(msg)


class ApiNotFoundError(ApiError):
    ...  # noqa: WPS428 WPS604
