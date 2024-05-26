import random
from .base_device import Sensor


class ColdWaterSensor(Sensor):
    def __init__(
            self,
            apartment: int,
    ):
        super().__init__(
            apartment,
            "coldwater",
            self.value_generator,
            60
        )

    def value_generator(self, value: int):
        if value == -1:
            return random.randrange(2, 200)

        return value + random.randrange(1, 10)
