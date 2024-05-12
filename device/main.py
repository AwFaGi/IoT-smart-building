from device.cold_water import ColdWaterSensor
from device.hot_water import HotWaterSensor
from device.temperature import TemperatureSensor
from device.conditioner import Conditioner
import sys


apartment = int(sys.argv[1])
port = int(sys.argv[2])
host_port = 8080


def eprint(message):
    print(message, file=sys.stderr)


hvs = ColdWaterSensor(apartment, host_port)
gvs = HotWaterSensor(apartment, host_port)
thermometer = TemperatureSensor(apartment, host_port)
conditioner = Conditioner(apartment, host_port, port)

threads = []

eprint(f'Initializing flat №{apartment}')
threads.append(hvs.start())
threads.append(gvs.start())
threads.append(thermometer.start())
threads.append(conditioner.start())

for t in threads:
    t.join()
