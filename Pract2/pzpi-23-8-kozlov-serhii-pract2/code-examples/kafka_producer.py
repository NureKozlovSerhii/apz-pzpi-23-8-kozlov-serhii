import json
from kafka import KafkaProducer


class SpotifyEventProducer:
    def __init__(self, broker_url='localhost:9092'):
        self.topic = 'spotify-user-activity'
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=[broker_url],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            self.is_connected = True
        except Exception as e:
            print("[Producer] Неможливо підключитися до Kafka. Режим імітації.")
            self.is_connected = False

    def emit_event(self, event_data: dict):
        if self.is_connected:
            self.producer.send(self.topic, event_data)
            self.producer.flush()

        print(f"[Event Producer] Подія '{event_data['event_type']}' надіслана у шину.")
