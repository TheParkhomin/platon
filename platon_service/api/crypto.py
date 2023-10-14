import hashlib
import jwt


class CryptoApi:

    def __init__(self, salt: str):
        self._salt = salt

    def create_hash(self, raw: str) -> str:
        password_raw = '{} {}'.format(raw, self._salt)
        secret = hashlib.sha256(password_raw.encode()).hexdigest()
        return secret

    def check_hash(self, secret: str, raw: str) -> bool:
        target_secret = self.create_hash(raw)
        return target_secret == secret


class JwtApi:
    _algorithm = "HS256"

    def __init__(self, secret: str):
        self._secret = secret

    def encode(self, payload: dict) -> str:
        encoded_jwt = jwt.encode(payload, self._secret, algorithm=self._algorithm)
        return encoded_jwt

    def decode(self, token: str) -> dict:
        payload = jwt.decode(token, self._secret, algorithms=self._algorithm)
        return payload
