from abc import ABC


class BaseTestLib(ABC):
    def recv_handler(self, message):
        pass
