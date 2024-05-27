import logging

from confluent_kafka.admin import AdminClient, NewTopic

from temperature import Temperature

admin_client = AdminClient({
    "bootstrap.servers": "kafka:9092"
})

topic_list = ["temperature", "coldwater", "hotwater"] + [f"conditioner{i}" for i in range(1, 101)]
admin_client.create_topics(
    [NewTopic(i, 1, 1) for i in topic_list]
)


def main():
    kafka_config = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'server',
        'auto.offset.reset': 'earliest'
    }

    temp_thread = Temperature(kafka_config)
    temp_thread.run().join()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
