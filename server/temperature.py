import json
import logging
import threading

from confluent_kafka import Consumer, Producer


class Temperature:
    def __init__(self, config):
        self.consumer = Consumer(config)
        self.producer = Producer(config)

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message)
        self.producer.flush()

    def build_message(self, state: int):
        return {
            "state": state
        }

    def process(self, message):
        if message["value"] > 24:
            msg = json.dumps(self.build_message(1))
            self.send_message(f"conditioner{message['apartment']}", msg)
        elif message["value"] < 18:
            msg = json.dumps(self.build_message(0))
            self.send_message(f"conditioner{message['apartment']}", msg)

    def listen(self):
        try:
            # подписываемся на топик
            self.consumer.subscribe(["temperature"])

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

