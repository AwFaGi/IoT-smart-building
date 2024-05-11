from device import Sensor, Valve
import sys
import random


apartment = int(sys.argv[1])
port = int(sys.argv[2])
host_port = 8080


def eprint(message):
    print(message, file=sys.stderr)


def cold_water_generator(value):
    if value == 0:
        return random.randrange(2, 200)

    return value + random.randrange(1, 10)


def hot_water_generator(value):
    if value == 0:
        return random.randrange(2, 30)

    return value + random.randrange(1, 3)


def temperature_generator(value):
    if value == 0:
        return random.randrange(20, 32)

    return value + random.randrange(-2, 2)


def conditioner_down():
    eprint("Conditioner is disabled")


def conditioner_up():
    eprint("Conditioner is enabled")


hvs = Sensor(apartment, "hvs", cold_water_generator, 8080)
gvs = Sensor(apartment, "gvs", hot_water_generator, 8080)
thermometer = Sensor(apartment, "thermo", temperature_generator, 8080)
conditioner = Valve(apartment, "cond", 8080, port, {"off": conditioner_down, "on": conditioner_up})

threads = []

eprint(f'Initializing flat №{apartment}')
threads.append(hvs.start())
threads.append(gvs.start())
threads.append(thermometer.start())
threads.append(conditioner.start())

for t in threads:
    t.join()
