import json
import logging
import threading
import time
from typing import Callable

from confluent_kafka import Producer, Consumer

logging.basicConfig(level=logging.DEBUG)

class Device:
    def __init__(self, apartment: int, device_type: str):
        self.apartment = apartment
        self.device_type = device_type

    def build_message(self, message_type: str, value: int = 0):
        return json.dumps({
            "apartment": self.apartment,
            "device_type": self.device_type,
            "message_type": message_type,
            "value": value
        })

    def start(self) -> threading.Thread:
        raise NotImplementedError


class Sensor(Device):
    def __init__(
            self,
            apartment: int,
            device_type: str,
            value_generator: Callable,
            timeout: int = 60
    ):
        super().__init__(apartment, device_type)
        self.value_generator = value_generator
        self.timeout = timeout
        self.is_running = True

        self.config = {
            'bootstrap.servers': 'kafka:9092',
            'auto.offset.reset': 'earliest'
        }

        self.producer = Producer(self.config)

    def value_generator(self, value: int) -> int:
        raise NotImplementedError

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message)
        self.producer.flush()

    def generate_value(self):
        value = -1
        while self.is_running:
            value = self.value_generator(value)
            self.send_message(self.device_type, self.build_message("data", value))
            time.sleep(self.timeout)

    def start(self):
        thread = threading.Thread(target=self.generate_value)
        thread.start()

        return thread

    def shutdown(self):
        self.is_running = False


class Valve(Device):
    def __init__(
            self,
            apartment: int,
            device_type: str,
            action: Callable
    ):
        super().__init__(apartment, device_type)
        self.action = action

        self.config = {
            'bootstrap.servers': 'kafka:9092',
            'group.id': f"{self.device_type}{self.apartment}",
            'auto.offset.reset': 'earliest'
        }

    def listen(self):
        consumer = Consumer(self.config)

        try:
            logging.debug("before")
            consumer.subscribe([f"{self.device_type}{self.apartment}"])
            logging.debug("after")

            while True:
                msg = consumer.poll()
                if msg is None:
                    continue
                if msg.error():
                    logging.error(msg.error())
                else:
                    value = msg.value().decode('utf-8')
                    logging.info(f"Received message: {value}")
                    self.action(json.loads(value))

        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    def start(self):
        thread = threading.Thread(target=self.listen)
        thread.start()

        return thread
