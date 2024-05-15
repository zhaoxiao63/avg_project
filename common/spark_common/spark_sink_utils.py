import psycopg2
from pyspark.sql import DataFrame
import pandas as pd

def upsert_to_postgres(df: DataFrame, epoch_id: int, db_params: dict, table_name: str, primary_key: list):
    """
    将 Spark DataFrame 写入 PostgreSQL 数据库，如果主键已存在则更新记录
    spark 自带 api 不支持 upsert 操作，自定义实现
    :param df:
    :param epoch_id:
    :param db_params:
    :param table_name:
    :param primary_key:
    :return:
    """

    columns = df.columns
    # columns 和 primary_key 的差集
    value_columns = [col for col in columns if col not in primary_key]

    pandas_df = df.toPandas()
    # 如果列名包含timestamp
    if 'timestamp' in columns:
        pandas_df['timestamp'] = pd.to_datetime(pandas_df['timestamp'], unit='ms')

    # 连接 PostgreSQL 数据库
    conn = psycopg2.connect(
        dbname=db_params["dbname"],
        user=db_params["user"],
        password=db_params["password"],
        host=db_params["host"],
        port=db_params["port"]
    )
    cursor = conn.cursor()

    # 定义 UPSERT 查询
    upsert_query = f"""
        INSERT INTO {table_name} {str(tuple(columns)).replace("'", "")}
        VALUES ({', '.join(['%s'] * len(columns))})
        ON CONFLICT ({', '.join(primary_key)})
        DO UPDATE SET
        {','.join([f"{column} = EXCLUDED.{column}" for column in value_columns])};
        """

    # 执行 UPSERT 操作
    for row in pandas_df.itertuples(index=False):
        cursor.execute(upsert_query, row)

    # 提交事务并关闭连接
    conn.commit()
    cursor.close()
    conn.close()


def insert_to_postgres(df: DataFrame, epoch_id: int, db_params: dict, table_name: str, write_mode: str ="append"):
    """
    将 Spark DataFrame 写入 PostgreSQL 数据库，覆盖已有记录
    :param write_mode:
    :param df:
    :param epoch_id:
    :param db_params:
    :param table_name:
    :return:
    """
    df.write \
        .jdbc(url=db_params["pg_uri"] + db_params["dbname"], table=table_name, mode=write_mode, properties=db_params)

