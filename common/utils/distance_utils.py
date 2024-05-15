import math
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType


# Haversine 公式计算距离的函数
def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # 地球半径，单位：公里

    # 将经纬度从度转换为弧度
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine 公式
    diff_lon = lon2 - lon1
    diff_lat = lat2 - lat1
    a = math.sin(diff_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


if __name__ == '__main__':
    # point 1 50.03, 5.42
    # point2 58.38, 3.04
    print(haversine(1, 1, 0.999, 0.999))
