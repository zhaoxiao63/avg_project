import logging

from kafka import KafkaProducer
import json


class KafkaProduct:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic, message):
        try:
            self.producer.send(topic, value=message)
            self.producer.flush()
            print(f"Message sent to topic {topic}: {message}")
        except Exception as e:
            print(f"Failed to send message to topic {topic}: {e}")

    def close(self):
        self.producer.close()
