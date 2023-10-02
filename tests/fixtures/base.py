from faker import Faker


class BaseDataGenerator:
    def __init__(self, fake: Faker) -> None:
        self._fake = fake
