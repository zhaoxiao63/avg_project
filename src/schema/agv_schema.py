from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType, LongType

agv_schema = StructType([
    StructField("agvId", StringType(), True),
    StructField("agvType", StringType(), True),
    StructField("routeId", StringType(), True),
    StructField("latitude", FloatType(), True),
    StructField("longitude", FloatType(), True),
    StructField("timestamp", LongType(), True),
    StructField("speed", FloatType(), True),
    StructField("fuelLevel", FloatType(), True)
])
