import logging

from confluent_kafka.admin import AdminClient, NewTopic

from listener import *

admin_client = AdminClient({
    "bootstrap.servers": "kafka:9092"
})

topic_list = ["temperature", "coldwater", "hotwater", "motion"]
cond_list = [f"conditioner{i}" for i in range(1, 101)]
light_list = [f"light{i}" for i in range(1, 101)]
admin_client.create_topics(
    [NewTopic(i, 1, 1) for i in topic_list + cond_list + light_list]
)


def main():
    kafka_config = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'server',
        'auto.offset.reset': 'earliest'
    }

    threads = []

    temp = Temperature(kafka_config)
    cold_water = ColdWater(kafka_config)
    hot_water = HotWater(kafka_config)
    motion = Motion(kafka_config)

    threads.append(temp.run())
    threads.append(cold_water.run())
    threads.append(hot_water.run())
    threads.append(motion.run())

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
