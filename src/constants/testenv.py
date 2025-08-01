class TestEnv:
    client_id = ""
    client_key = ""
    host = "localhost"
    port = "8000"

    # ids of projects belonging to this test client.
    projects = []

    def __init__(self):
        pass

    def configure(self, host, port, client_id=None, client_key=None):
        self.host = host
        self.port = port
        if self.client_id:
            self.client_id = client_id
            self.client_key = client_key

    def set_client(self, client_id, client_key):
        self.client_id = client_id
        self.client_key = client_key


testEnv = TestEnv()
