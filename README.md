# AGV_PROJECT

## 1.Set Up and Run the Project

```sh
# kafka postgre zookeeper（kafka依赖zk）
docker-compose -p agv_project up -d
```

## 2.Check the Project's Running Status

```sh
docker stats
```

## 3.Verify PG Database Data

1. Enter the PostgreSQL database Docker interface

```sh
docker exec -it agv_project-postgres-1 bash
```

2. Connect to the PostgreSQL database

```sh
psql -U postgres
```

3. View databases

```sql
\l
```

4. Connect to a specific database

```sql
\c agv_traffic_db
```

5. View project tables

```sql
\dt
```

6. View project table data

```sql
-- AGVs within 2000 km of the factory center
select * from agv_poi_traffic limit 10;

-- Number of AGVs on a specific route at a specific time point
select * from agv_total_traffic limit 10;

-- Number of AGVs on a specific route in the last 30 seconds
select * from agv_window_traffic limit 10;
```



## 4.Project Configuration

Configuration file location: `config/agv_config.py`

```python
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
```

