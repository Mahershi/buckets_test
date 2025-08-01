import httpx


class HttpClient:
    @staticmethod
    async def get(url, headers={}, query_params={}):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=query_params)
                return {
                    "status_code": response.status_code,
                    "data": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
                }
        except Exception as e:
            print(f"HttpClient get Exception: {e}")
            return {}

    @staticmethod
    async def post(url, headers={}, query_params={}, data={}):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, params=query_params, json=data)
                return {
                    "status_code": response.status_code,
                    "data": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
                }
        except Exception as e:
            print(f"HttpClient post Exception: {e}")
            return {}
