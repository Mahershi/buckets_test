import time
import asyncio
from src.utils.helpers import Helpers


async def test_client_login():
    resp = await Helpers.get_client_token()
    print(resp)

asyncio.run(test_client_login())

#
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0MDU4OTkwLCJpYXQiOjE3NTM5NzI1OTAsImp0aSI6ImMzNDgwNWUzOGZiMjQ3YWZhNzhjMjJjNzU4YmRhOTQwIiwiY2xpZW50X2lkIjo1OTQ0fQ.1NhbaqAwPp1VDiFj2gK4DzjsaNzvL49702GzTfDc5Ms"
#
#
# auth_msg = {
#     "type": "authentication",
#     "data": {
#         "authentication": f"Bearer {token}"
#     }
# }
# def recv(msg):
#     print(msg)
#
#
# async def test():
#     client = WSClient(uri="ws://localhost:8000/project/stream/1203/", recv_handler=recv)
#     await client.connect()
#     await asyncio.sleep(2)
#     await client.send_json(auth_msg)
#     await asyncio.sleep(5)
#     await client.close()
#
#
# asyncio.run(test())
#
# time.sleep(15)