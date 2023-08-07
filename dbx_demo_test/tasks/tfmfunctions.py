import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

# Because this file is not a Databricks notebook, you
# must create a Spark session. Databricks notebooks
# create a Spark session for you by default.
spark = SparkSession.builder \
                    .appName('integrity-tests') \
                    .getOrCreate()


def transform_data(input_df):
    transformed_df = (input_df.groupBy('cn',).agg(count('device_id').alias('TotalDeviceIds')).orderBy(col('TotalDeviceIds').desc()).limit(5))
    return transformed_df