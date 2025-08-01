from .basetestlib import BaseTestLib


class BaseWSTestLib(BaseTestLib):
    def recv_handler(self, message):
        print(message)
