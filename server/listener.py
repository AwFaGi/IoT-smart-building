import json
import logging
import threading
import copy

from confluent_kafka import Consumer, Producer


class BasicListener:

    def __init__(self, config, topic):
        self.config = copy.deepcopy(config)
        self.config['group.id'] += f"-{topic}"
        self.consumer = Consumer(self.config)
        self.topic = topic

    def build_message(self, state: int):
        return {
            "state": state
        }

    def process(self, message):
        raise NotImplementedError

    def listen(self):
        try:
            # подписываемся на топик
            self.consumer.subscribe([self.topic])

            while True:
                msg = self.consumer.poll()
                if msg is None:
                    continue
                if msg.error():
                    logging.error(msg.error())
                else:
                    value = msg.value().decode('utf-8')
                    logging.info(f"Received message: {value}")
                    self.process(json.loads(value))

        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()

    def run(self) -> threading.Thread:
        thread = threading.Thread(target=self.listen)
        thread.start()

        return thread


class Temperature(BasicListener):
    def __init__(self, config):
        super().__init__(config, "temperature")
        self.producer = Producer(config)

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message)
        self.producer.flush()

    def process(self, message):
        if message["value"] > 24:
            msg = json.dumps(self.build_message(1))
            self.send_message(f"conditioner{message['apartment']}", msg)
        elif message["value"] < 18:
            msg = json.dumps(self.build_message(0))
            self.send_message(f"conditioner{message['apartment']}", msg)


class Motion(BasicListener):
    def __init__(self, config):
        super().__init__(config, "motion")
        self.producer = Producer(config)

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message)
        self.producer.flush()

    def process(self, message):
        if message["value"] == 1:
            msg = json.dumps(self.build_message(1))
            self.send_message(f"light{message['apartment']}", msg)
        elif message["value"] == 0:
            msg = json.dumps(self.build_message(0))
            self.send_message(f"light{message['apartment']}", msg)


class ColdWater(BasicListener):
    def __init__(self, config):
        super().__init__(config, "coldwater")

    def process(self, message):
        logging.info(f"Registering cold water: flat {message['apartment']}, value {message['apartment']}")


class HotWater(BasicListener):
    def __init__(self, config):
        super().__init__(config, "hotwater")

    def process(self, message):
        logging.info(f"Registering hot water: flat {message['apartment']}, value {message['apartment']}")