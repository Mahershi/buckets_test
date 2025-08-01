import asyncio
import time
from typing import List

from src.constants.testenv import testEnv
from src.tests.BaseTest import BaseTest
from src.libs import WSClient


class WSConnectionConcurrentTest(BaseTest):
    ITERATIONS = 1
    CONCURRENT_CLIENTS = 100
    CONNECTION_TIMEOUT = 5      # seconds, need to be less than 10 as that is the auth timeout.
    clients = []
    BREATHE_TIME = 3    # seconds, sleep time between iterations

    def setup(self):
        wsurl = self.testParams.get('url')
        self.CONCURRENT_CLIENTS = self.testParams.get("concurrent", 100)
        self.ITERATIONS = self.testParams.get("iterations", 1)
        if not wsurl:
            raise Exception("wsUrl not provided")

        self.clients = [
            WSClient(uri=wsurl, recv_handler=self.testLib.recv_handler)
            for _ in range(self.CONCURRENT_CLIENTS)
        ]

    # pass the client for which the steps need to be run.
    # will be called for each clients
    # Default return True to show steps passed.
    async def handle_steps(self, client):
        return True

    async def run_concurrent_clients(self) -> List[bool]:
        start_event = asyncio.Event()
        ready_counter = asyncio.Semaphore(0)

        tasks = [
            asyncio.create_task(
                self.run_client(client, i, None, start_event, ready_counter)
            )
            for i, client in enumerate(self.clients)
        ]

        for _ in range(self.CONCURRENT_CLIENTS):
            await ready_counter.acquire()

        start_event.set()
        return await asyncio.gather(*tasks)

    async def run_client(self, client, index, ready_event: asyncio.Event, start_event: asyncio.Event, ready_counter: asyncio.Semaphore):
        try:
            # Mark self as ready
            print("running client")
            ready_counter.release()
            print(f"[{index}] released Semaphore - READY and WAITING")
            await start_event.wait()

            await client.connect()
            print(f"[{index}] Connected")
            passed = await self.handle_steps(client)
            print(f"Awaiting connection timeout {self.CONNECTION_TIMEOUT}s before closing.")
            await asyncio.sleep(self.CONNECTION_TIMEOUT)
            await client.close()
            print(f"[{index}] Closed")
            return passed
        except Exception as e:
            print(f"[{index}] Failed: {e}")
            return False

    async def execute(self):
        overall_results = []

        for itr in range(self.ITERATIONS):
            print(f"\n--- Iteration {itr + 1} ---")
            results = await self.run_concurrent_clients()
            overall_results.extend(results)
            time.sleep(self.BREATHE_TIME)
        if all(overall_results):
            self.setPass()
        else:
            self.setFail()

    def cleanup(self):
        pass

    def resolve_param(self, param: str, client):
        if not isinstance(param, str):
            return param
        if not (param.startswith("{") and param.endswith("}")):
            return param

        key = param.strip("{}")

        # Priority: testEnv > self > client
        if hasattr(testEnv, key):
            return getattr(testEnv, key)
        elif hasattr(self, key):
            return getattr(self, key)
        elif hasattr(client, key):
            return getattr(client, key)
        else:
            return param
