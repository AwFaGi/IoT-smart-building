import random
from device import Sensor


class ColdWaterSensor(Sensor):
    def __init__(
            self,
            apartment: int,
            host_port: int,
    ):
        super().__init__(
            apartment,
            "hvs",
            self.value_generator,
            host_port,
            60
        )

    def value_generator(self, value: int):
        if value == 0:
            return random.randrange(2, 200)

        return value + random.randrange(1, 10)
