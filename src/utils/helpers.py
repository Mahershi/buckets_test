from src.constants.testenv import testEnv
from src.constants.apis import API
from src.libs.httpclient import HttpClient
import asyncio


class Helpers:
    @staticmethod
    async def get_client_token():
        resp = await Helpers.login_client()
        if resp.get('status_code', None) == 200:
            return resp['data']['access']

    @staticmethod
    async def login_client():
        testEnv.set_client("b07c4d0709dc7b3cfaa3bc6a4b80cc5a", "W8nmcKwxEdc_KZqYVxhLXqU5rcb30gznN21UBUD66uE")
        return await HttpClient.post(
            url=f"http://{testEnv.host}:{testEnv.port}{API.GET_CLIENT_TOKEN}",
            data={
                "client_id": testEnv.client_id,
                "client_key": testEnv.client_key
            }
        )