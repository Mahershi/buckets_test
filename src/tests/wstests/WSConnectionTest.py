import time

from src.tests.BaseTest import BaseTest
from src.libs import WSClient
from src.constants.testenv import testEnv


class WSConnectionTest(BaseTest):
    client = None
    ITERATIONS = 1
    BREATHE_TIME = 0.5

    def setup(self):
        print(testEnv.client_id)
        wsurl = self.testParams.get('url')
        if not wsurl:
            raise Exception("wsUrl not provided")
        self.client = WSClient(uri=wsurl, recv_handler=self.testLib.recv_handler)

    async def execute(self):
        try:
            for itr in range(self.ITERATIONS):
                print(f"Iteration {itr}")
                await self.client.connect()
                await self.client.close()
                time.sleep(self.BREATHE_TIME)
            self.setPass()
        except Exception as e:
            print(f"Test failed at iteration {itr}: {e}")
            self.setFail()

    def cleanup(self):
        pass


class WSConnectionTest100Iter(WSConnectionTest):
    ITERATIONS = 100



