import logging
import sys

from device.cold_water import ColdWaterSensor
from device.hot_water import HotWaterSensor
from device.conditioner import Conditioner
from device.temperature import TemperatureSensor
from device.light import Light
from device.motion import MotionSensor


def main():
    apartment = int(sys.argv[1])

    hvs = ColdWaterSensor(apartment)
    gvs = HotWaterSensor(apartment)
    conditioner = Conditioner(apartment)
    thermometer = TemperatureSensor(apartment)
    light = Light(apartment)
    motion = MotionSensor(apartment)

    threads = []

    logging.debug(f'Initializing flat №{apartment}')
    threads.append(hvs.start())
    threads.append(gvs.start())
    threads.append(conditioner.start())
    threads.append(thermometer.start())
    threads.append(light.start())
    threads.append(motion.start())

    for t in threads:
        t.join()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
