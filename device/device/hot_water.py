import random
from .base_device import Sensor


class HotWaterSensor(Sensor):
    def __init__(
            self,
            apartment: int,
            host_port: int,
    ):
        super().__init__(
            apartment,
            "gvs",
            self.value_generator,
            host_port,
            60
        )

    def value_generator(self, value: int):
        if value == 0:
            return random.randrange(2, 30)

        return value + random.randrange(1, 3)
