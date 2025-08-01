class BaseParams:
    params = None

    def __init__(self, json):
        self.params = json

    def get(self, key, default=None):
        return self.params.get(key, default)