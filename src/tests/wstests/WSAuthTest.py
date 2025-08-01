from .ConcurrentWSConnectionTest import WSConnectionConcurrentTest
from src.utils.parser import load_template, message_matches
from src.utils.helpers import Helpers


class WSAuthTest(WSConnectionConcurrentTest):
    client_token = None

    async def execute(self):
        self.client_token = await Helpers.get_client_token()
        await super().execute()

    async def run_step(self, client, step):
        print(f"Running Step: {step}")
        send = step.get("send")
        recv = step.get("recv")

        if send:
            template_key = send.get('template', None)
            params = send.get('params', [])
            resolved_params = [self.resolve_param(p, client) for p in params]
            print(f"Resolved Params: {resolved_params}")
            payload = load_template(template_key, resolved_params)
            print(f"Send Payload: {payload}")
            await client.send_json(payload)

        if recv:
            expect_count = recv.get('expect', len(self.clients))
            expect_count = int(expect_count)
            print(f"Expected {expect_count} number of receive message(s)")
            template_key = recv.get('template', None)
            params = recv.get('params', [])
            expect_payload = load_template(template_key, params)
            print(f"Waiting for expect_payload: {expect_payload}")
            for i in range(expect_count):
                msg = await client.recv(timeout=3)
                match = message_matches(
                    actual=msg,
                    expected_template=expect_payload
                )
                if not match:
                    raise AssertionError(f"Message mismatch:\nExpected: {expect_payload}\nActual: {msg}")
                else:
                    print("Matching payload received")

    async def handle_steps(self, client):
        for step in self.testParams.get('steps', []):
            try:
                await self.run_step(client, step)
            except Exception as e:
                print(f"[Client Error] Step failed: {e}")
                return False
        return True
