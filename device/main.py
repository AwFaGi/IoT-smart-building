import logging

from device.cold_water import ColdWaterSensor
from device.hot_water import HotWaterSensor
from device.temperature import TemperatureSensor
from device.conditioner import Conditioner
import sys


apartment = int(sys.argv[1])
port = int(sys.argv[2])
host_port = 8080

logging.basicConfig(level=logging.DEBUG)

hvs = ColdWaterSensor(apartment)
gvs = HotWaterSensor(apartment)
thermometer = TemperatureSensor(apartment)
conditioner = Conditioner(apartment)

threads = []

logging.debug(f'Initializing flat №{apartment}')
threads.append(hvs.start())
threads.append(gvs.start())
threads.append(thermometer.start())
threads.append(conditioner.start())

for t in threads:
    t.join()
