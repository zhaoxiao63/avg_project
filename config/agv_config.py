CONFIG = {
    "PG_CONFIG": {
        "user": "postgres",
        "password": "postgres",
        "driver": "org.postgresql.Driver",
        "host": "localhost",
        "port": "5432",
        "dbname": "agv_traffic_db",
        "pg_uri": "jdbc:postgresql://localhost:5432/"
    },
    "AGV_TOPIC": "my_agv_topic",
    "KAFKA_CONFIG": {
        "bootstrap.servers": "localhost:9092",
        "session.timeout.ms": 3600000,
        "max.poll.interval.ms": 3600000,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False
    }
}

if __name__ == '__main__':
    import json

    print(json.dumps(CONFIG))
