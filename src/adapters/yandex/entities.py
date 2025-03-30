from dataclasses import dataclass
from datetime import date, datetime


class APIException(Exception):
    pass


@dataclass
class UserInfo:
    id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    birthday: date | None = None

    @classmethod
    def parse(cls, response: dict):
        return cls(
            id=response.get("id"),
            first_name=response.get("first_name"),
            last_name=response.get("last_name"),
            email=response.get("default_email"),
            phone=response.get("default_phone", {}).get("number"),
            birthday=(
                datetime.strptime(response["birthday"], "%Y-%m-%d")
                if response.get("birthday")
                else None
            ),
        )
