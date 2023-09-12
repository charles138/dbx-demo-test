import pyspark
from dbx_demo_test.tasks.tfmfunctions import *
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import logging


input_df = spark.read.json("/databricks-datasets/iot/iot_devices.json")
transformed_df = transform_data(input_df)

expected_schema = StructType([
            StructField('cn', StringType(), True),
            StructField('TotalDeviceIds', LongType(), False)
            ])

expected_data = [("United States", 68545),
                    ("China", 14455),
                    ("Japan", 12100),
                    ("Republic of Korea", 11879),
                    ("Germany", 7942)]

expected_df = spark.createDataFrame(data=expected_data, schema=expected_schema)


def test_schema():
  assert(expected_df.schema == transformed_df.schema)

def test_df():
  assert sorted(expected_df.collect()) == sorted(transformed_df.collect())

def test_rowcount():
  assert expected_df.count() == 5

