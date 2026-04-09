import json
from kafka import KafkaConsumer


class CassandraMockDB:
    def __init__(self):
        self.play_history = []

    def insert_event(self, event: dict):
        self.play_history.append(event)
        print(f"[Cassandra DB] Запис збережено. Всього: {len(self.play_history)}")


class AnalyticsWorker:
    def __init__(self, broker_url='localhost:9092'):
        self.topic = 'spotify-user-activity'
        self.db = CassandraMockDB()

        try:
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=[broker_url],
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id='analytics-consumer-group'
            )
        except Exception:
            self.consumer = None

    def run(self):
        print("[Analytics Service] Запущено. Очікування подій...")

        if not self.consumer:
            return

        for message in self.consumer:
            event = message.value

            if event.get('event_type') == 'TRACK_PLAYED':
                print(f"[Analytics] Оброблено подію від користувача {event['user_id']}")
                self.db.insert_event(event)


if __name__ == "__main__":
    worker = AnalyticsWorker()
    worker.run()
