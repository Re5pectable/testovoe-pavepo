from datetime import datetime, timedelta, timezone
from jose import jwt

from .. import config


class Token:
    def __init__(self, claims: dict, expires: datetime):
        self.claims = claims
        self.expires = expires

    @classmethod
    def from_jwt(cls, token_str: str) -> "Token":
        decoded = jwt.decode(token_str, config.JWT_SECRET, algorithms=[config.JWT_ALGO])
        expires = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        return cls(decoded, expires)

    def to_jwt(self) -> str:
        to_encode = self.claims | {"exp": self.exp}
        return jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGO)

    @property
    def exp(self) -> int:
        return int(self.expires.timestamp())


class AccessToken(Token):
    def __init__(self, claims: dict):
        expires = datetime.now() + timedelta(
            seconds=config.JWT_ACCESS_EXP_SEC
        )
        super().__init__(claims, expires)


class RefreshToken(Token):
    def __init__(self, claims: dict):
        expires = datetime.now() + timedelta(
            seconds=config.JWT_REFRESH_EXP_SEC
        )
        super().__init__(claims, expires)
