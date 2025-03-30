import os
from pathlib import Path


def _env2bool(key, default=None):
    val = os.getenv(key, default)
    r_val = {
        "true": True,
        "1": True,
        "false": False,
        "0": False,
    }.get(val.lower())
    if not r_val:
        raise ValueError(f"Cannot parse boolean variable {key} (value: {val})")
    return r_val


def _env2int(key, default=None):
    val = os.getenv(key, default)
    try:
        return int(val)
    except Exception:
        raise ValueError(f"Cannot parse integer variable {key} (value: {val})")


DEBUG: bool = _env2bool("DEBUG", "true")

DB_HOST: str = os.getenv("DB_HOST")
DB_NAME: str = os.getenv("DB_NAME")
DB_USERNAME: str = os.getenv("DB_USERNAME")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_URL: str = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

YANDEX_OAUTH_SECRET = os.getenv("YANDEX_OAUTH_SECRET")
YANDEX_OAUTH_CLIENTID = os.getenv("YANDEX_OAUTH_CLIENTID")

JWT_ALGO: str = os.getenv("JWT_ALGO", "HS256")
JWT_SECRET: str = os.getenv("JWT_SECRET_KEY")
JWT_ACCESS_EXP_SEC: int = _env2int("JWT_ACCESS_EXP_SEC", 60 * 15)
JWT_REFRESH_EXP_SEC: int = _env2int("JWT_REFRESH_EXP_SEC", 60 * 60 * 24 * 3)

MEDIA_PATH = os.path.dirname(os.path.realpath(__name__)) + "/media"
Path(MEDIA_PATH).mkdir(parents=True, exist_ok=True)

ALLOW_CORS_FROM: list[str] = os.getenv("ALLOW_CORS_FROM", "").split(";")
