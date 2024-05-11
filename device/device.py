from bottle import Bottle, run
import time
from typing import Callable
import requests
import threading


class Device:
    def __init__(self, apartment: int, device_type: str, host_port: int):
        self.apartment = apartment
        self.device_type = device_type
        self.host = f"http://host.docker.internal:{host_port}/{device_type}"

    def build_message(self, message_type: str, value: int = 0):
        return {
            "apartment": self.apartment,
            "device_type": self.device_type,
            "message_type": message_type,
            "value": value
        }

    def hello_server(self):
        requests.post(self.host, self.build_message("hello"))

    def start(self) -> threading.Thread:
        raise NotImplementedError


class Sensor(Device):
    def __init__(
            self,
            apartment: int,
            device_type: str,
            value_generator: Callable,
            host_port: int,
            timeout: int = 60
    ):
        super().__init__(apartment, device_type, host_port)
        self.value_generator = value_generator
        self.timeout = timeout
        self.is_running = True

    def generate_value(self):
        self.hello_server()
        value = -1
        while self.is_running:
            value = self.value_generator(value)
            requests.post(self.host, self.build_message("data", value))
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
            host_port: int,
            port: int,
            actions: dict[str, Callable]

    ):
        super().__init__(apartment, device_type, host_port)
        self.actions = actions
        self.port = port

    def listen(self):
        self.hello_server()
        app = Bottle()

        @app.route('/actions/<action>')
        def actions(action):
            self.actions[action]()
            return "OK!"

        run(app, host='0.0.0.0', port=self.port)

    def start(self):
        thread = threading.Thread(target=self.listen)
        thread.start()

        return thread
