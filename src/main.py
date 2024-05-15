from pyspark.sql import Window
from pyspark.sql.functions import from_json, col, date_format, window, count, max, row_number
from pyspark.sql.types import DoubleType

from common.utils.distance_utils import haversine
from config.agv_config import CONFIG
from common.spark_common.spark_utils import get_spark_session, columns_mapping
from common.spark_common.spark_source_utils import get_kafka_source
from common.spark_common.spark_sink_utils import upsert_to_postgres, insert_to_postgres
from schema import agv_schema

if __name__ == "__main__":
    # 创建 SparkSession
    spark = get_spark_session("agv_project", "local[*]")

    # 注册 udf 函数
    spark.udf.register("haversine", haversine, DoubleType())

    # Kafka 配置
    kafka_bootstrap_servers = CONFIG["KAFKA_CONFIG"]["bootstrap.servers"]
    kafka_topic = CONFIG["AGV_TOPIC"]

    # 从 Kafka 读取数据
    source_df = get_kafka_source(spark, kafka_bootstrap_servers, kafka_topic)

    # 对数据进行解析
    parsed_df = source_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), agv_schema.agv_schema).alias("agv_data")) \
        .select("agv_data.*") \
        .withColumn("timestamp", (col("timestamp") / 1000).cast("timestamp")) \
        .withColumn("record_date", date_format("timestamp", "yyyy-MM-dd")) \

    # 将列名转换为下划线命名
    parsed_df = columns_mapping(parsed_df)

    # 聚合当天每个线路每种车型的总数
    agv_total_traffic = parsed_df.groupBy("record_date", "route_id", "agv_type") \
        .agg(count("*").alias("total_count"), (max("timestamp").cast("long")*1000).alias("timestamp")) \
        .selectExpr("route_id", "agv_type as vehicle_type", "total_count", "timestamp", "record_date") \
        .writeStream \
        .outputMode("update") \
        .foreachBatch(lambda df, epoch_id: upsert_to_postgres(df,
                                                              epoch_id,
                                                              CONFIG["PG_CONFIG"],
                                                              "agv_total_traffic",
                                                              ["record_date", "route_id", "vehicle_type"])) \
        .start()

    # 滚动窗口的滚动时间为 30s
    agv_window = window("timestamp", "30 seconds")

    # 每30s聚合每个线路每种车型的总数
    agv_30s_window_traffic = parsed_df.groupBy(agv_window, "record_date", "route_id", "agv_type") \
        .agg(count("*").alias("total_count"), max("timestamp").alias("timestamp")) \
        .selectExpr("route_id", "agv_type as vehicle_type", "total_count", "timestamp", "record_date") \
        .writeStream \
        .outputMode("complete") \
        .foreachBatch(lambda df, epoch_id: insert_to_postgres(df,
                                                              epoch_id,
                                                              CONFIG["PG_CONFIG"],
                                                              "agv_window_traffic",
                                                              "overwrite")) \
        .start()

    # 获取小车距离中心工程的距离 由于随机生成的距离都太大，这里设置为 2000km
    agv_poi_traffic = parsed_df.select("agv_id", "agv_type", "latitude", "longitude", "timestamp") \
        .selectExpr("agv_id as vehicle_id",
                    "agv_type as vehicle_type",
                    "haversine(1, 1, longitude, latitude) as distance",
                    "timestamp") \
        .filter("distance < 2000") \
        .writeStream \
        .outputMode("append") \
        .foreachBatch(lambda df, epoch_id: insert_to_postgres(df,
                                                              epoch_id,
                                                              CONFIG["PG_CONFIG"],
                                                              "agv_poi_traffic",
                                                              "append")) \
        .start()

    agv_total_traffic.awaitTermination()
    agv_30s_window_traffic.awaitTermination()
    agv_poi_traffic.awaitTermination()
