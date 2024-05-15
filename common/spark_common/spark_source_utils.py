from pyspark.sql import SparkSession


def get_kafka_source(spark: SparkSession, kafka_bootstrap_servers, kafka_topic):
    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .option("startingOffsets", "latest") \
        .load()
