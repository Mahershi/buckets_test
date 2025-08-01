import asyncio
import json

import websockets


class WSClient:
    def __init__(self, uri: str, recv_handler=None):
        self.uri = uri
        self.connection = None
        self.recv_handler = recv_handler
        self.recv_queue = asyncio.Queue()
        self.keep_running = True
        self.recv_task = None

    # @property
    # def connected(self):
    #     return self.connection is not None and not self.connection.closed

    async def connect(self):
        try:
            self.connection = await websockets.connect(self.uri)
            print(f"WS Connected: {self.uri}")
            self.recv_task = asyncio.create_task(self._receive_loop())
        except Exception as e:
            print(f"Failed to connect: {e}")
            raise

    async def send(self, message: str):
        print(f"WS send, message: {message}")
        if not self.connection:
            raise RuntimeError("WebSocket not Connected")
        await self.connection.send(message)

    async def send_json(self, message: dict):
        await self.send(message=json.dumps(message))

    async def recv(self, timeout=None, parse_json=True):
        try:
            if timeout:
                msg = await asyncio.wait_for(self.recv_queue.get(), timeout=timeout)
            else:
                msg = await self.recv_queue.get()
            return json.loads(msg) if parse_json else msg
        except asyncio.TimeoutError:
            print("Timeout waiting for message.")
            return None
        except json.JSONDecodeError:
            print("Failed to decode JSON message.")
            return None

    async def _receive_loop(self):
        print(f"WS Recv Loop Started: {self.uri}")
        try:
            while self.keep_running:
                msg = await self.connection.recv()
                await self.recv_queue.put(msg)
                if self.recv_handler:
                    try:
                        self.recv_handler(msg)
                    except Exception as e:
                        print(f"Error in recv_handler: {e}")
        except websockets.ConnectionClosed:
            print("Connection closed in receiver.")
        except Exception as e:
            print(f"Receiver error: {e}")
        print(f"WS Recv Loop Stopped: {self.uri}")

    async def close(self):

        self.keep_running = False
        if self.recv_task:
            self.recv_task.cancel()
            try:
                await self.recv_task
            except asyncio.CancelledError:
                pass
        if self.connection:
            await self.connection.close()
        print(f"WS Closed: {self.uri}")
