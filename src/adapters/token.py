from datetime import datetime, timedelta
from jose import jwt

from .. import config


class Token:
    lifetime: timedelta = timedelta(seconds=0)

    def __init__(self, claims: dict, expires: datetime = None):
        self.claims = claims
        self.expires = expires or (datetime.now() + self.lifetime)

    @classmethod
    def from_jwt(cls, token_str: str) -> "Token":
        decoded = jwt.decode(token_str, config.JWT_SECRET, algorithms=[config.JWT_ALGO])
        expires = datetime.fromtimestamp(decoded["exp"])
        return cls(decoded, expires=expires)

    def to_jwt(self) -> str:
        to_encode = self.claims | {"exp": self.exp}
        return jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGO)

    @property
    def exp(self) -> int:
        return int(self.expires.timestamp())


class AccessToken(Token):
    lifetime: timedelta = timedelta(seconds=config.JWT_ACCESS_EXP_SEC)


class RefreshToken(AccessToken):
    lifetime: timedelta = timedelta(seconds=config.JWT_REFRESH_EXP_SEC)
