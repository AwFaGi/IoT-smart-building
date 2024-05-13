import random
from .base_device import Sensor


class TemperatureSensor(Sensor):
    def __init__(
            self,
            apartment: int,
            host_port: int,
    ):
        super().__init__(
            apartment,
            "thermo",
            self.value_generator,
            host_port,
            20
        )

    def value_generator(self, value: int):
        if value == 0:
            return random.randrange(20, 32)

        return value + random.randrange(-2, 2)
