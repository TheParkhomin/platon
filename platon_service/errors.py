class ExpectedError(Exception):
    pass


class InsufficientFunds(ExpectedError):
    def __init__(self, source_id: int, value: int):
        super().__init__(f'Insufficient funds for wallet {source_id}, amount: {value}')

