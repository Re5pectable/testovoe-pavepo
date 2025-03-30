from httpx import AsyncClient

from .entities import APIException, UserInfo


async def get_user_info(oauth_token: str) -> UserInfo:
    """
    https://yandex.ru/dev/id/doc/en/user-information
    """
    async with AsyncClient() as c:
        headers = {"Authorization": f"OAuth {oauth_token}"}
        response = await c.get(
            "https://login.yandex.ru/info?format=json", headers=headers
        )
        if response.status_code != 200:
            raise APIException(response.text)

        return UserInfo.parse(response.json())
