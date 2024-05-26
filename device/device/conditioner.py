import logging

from .base_device import Valve


class Conditioner(Valve):
    def __init__(
            self,
            apartment: int,
    ):
        super().__init__(
            apartment,
            "conditioner",
            self.process_message
        )
        logging.basicConfig(level=logging.DEBUG)

    def process_message(self, message):
        if message["state"] == 1:
            logging.info("Conditioner enabled")
        elif message["state"] == 0:
            logging.info("Conditioner disabled")

