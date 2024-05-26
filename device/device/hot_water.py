import random
from .base_device import Sensor


class HotWaterSensor(Sensor):
    def __init__(
            self,
            apartment: int,
    ):
        super().__init__(
            apartment,
            "hotwater",
            self.value_generator,
            60
        )

    def value_generator(self, value: int):
        if value == -1:
            return random.randrange(2, 30)

        return value + random.randrange(1, 3)
