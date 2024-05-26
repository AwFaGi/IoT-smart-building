import random
from .base_device import Sensor


class TemperatureSensor(Sensor):
    def __init__(
            self,
            apartment: int,
    ):
        super().__init__(
            apartment,
            "temperature",
            self.value_generator,
            20
        )

    def value_generator(self, value: int):
        if value == -1:
            return random.randrange(16, 32)

        return value + random.randrange(-2, 2)
