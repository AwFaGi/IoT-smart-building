import random
from .base_device import Sensor


class MotionSensor(Sensor):
    def __init__(
            self,
            apartment: int,
    ):
        super().__init__(
            apartment,
            "motion",
            self.value_generator,
            20
        )

    def value_generator(self, value: int):
        if random.random() > 0.8:
            return 1
        else:
            return 0
