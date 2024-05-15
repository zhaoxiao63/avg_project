import uuid
import random
import time
import json
from common.kafka_common.kafka_producer import KafkaProduct
from config.agv_config import CONFIG


def generate_data():
    """
    生成agv data
    agvId: 字符串类型， 可以是UUID
    agvType: 枚举类型， 为LARGE，MEDIUM， SMALL， TINY
    routeId: 字符串类型， 为'route-'+数字， 数字为00~49,
    latitude: 整形，地理信息的经度
    longitude: 整形，地理信息的纬度
    timestamp: 当前时间戳
    speed: 为车速
    fuelLevel: 电量
    :return: json
    """
    agvId = str(uuid.uuid4())
    agvType = random.choice(['LARGE', 'MEDIUM', 'SMALL', 'TINY'])
    routeId = f'route-{random.randint(0, 49):02d}'
    latitude = round(random.uniform(-90.0, 90.0))
    longitude = round(random.uniform(-180.0, 180.0))
    timestamp = int(time.time() * 1000)
    speed = round(random.uniform(0, 100), 1)
    fuelLevel = round(random.uniform(0, 100), 1)

    agv_data = {
        "agvId": agvId,
        "agvType": agvType,
        "routeId": routeId,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": timestamp,
        "speed": speed,
        "fuelLevel": fuelLevel
    }
    return agv_data


if __name__ == "__main__":
    producer = KafkaProduct(CONFIG["KAFKA_CONFIG"]["bootstrap.servers"])
    while True:
        data = generate_data()
        producer.send_message(CONFIG["AGV_TOPIC"], data)
        time.sleep(0.1)
