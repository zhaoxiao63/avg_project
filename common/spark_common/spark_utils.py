from pyspark.sql import SparkSession, DataFrame
from common.utils.columns_utils import camel_to_snake


def get_spark_session(app_name: str, master: str) -> SparkSession:
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.jars",
                "../../dependencies/jars/spark-token-provider-kafka-0-10_2.12-3.1.1.jar,"
                "../../dependencies/jars/spark-sql-kafka-0-10_2.12-3.1.1.jar,"
                "../../dependencies/jars/kafka-clients-2.7.0.jar,"
                "../../dependencies/jars/commons-pool2-2.11.1.jar,"
                "../../dependencies/jars/postgresql-42.2.20.jar") \
        .config("spark.streaming.kafka.consumer.poll.ms", "1000") \
        .master(master) \
        .getOrCreate()


def columns_mapping(df: DataFrame) -> DataFrame:
    """
    将 DataFrame 的列名转换为下划线命名
    :param df:
    :return:
    """
    for column in df.columns:
        df = df.withColumnRenamed(column, camel_to_snake(column))
    return df
