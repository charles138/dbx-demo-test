import pytest
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
row_count = 11
str_schema = "StructType([StructField('MedInc', DoubleType(), True), StructField('HouseAge', LongType(), True), StructField('AveRooms', DoubleType(), True), StructField('AveBedrms', DoubleType(), True), StructField('Population', LongType(), True), StructField('AveOccup', DoubleType(), True), StructField('Latitude', DoubleType(), True), StructField('Longitude', DoubleType(), True), StructField('MedHouseVal', DoubleType(), True)])"
df = spark.read.table('default.sklearn_housing')
# assert df.count() == row_count
# assert str(df.schema) == str_schema

@pytest.fixture
def table_input_df():
    return spark.read.table('default.sklearn_housing')

def test_table_row_count(table_input_df):  
    assert table_input_df.count() == row_count

def test_table_schema(table_input_df):  
    assert str(table_input_df.schema) == str_schema