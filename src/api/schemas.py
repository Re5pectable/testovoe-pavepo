from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: str | None = None


class AccessToken(BaseModel):
    access_token: str
