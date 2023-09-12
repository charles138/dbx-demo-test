import pyspark
from dbx_demo_test.tasks.tfmfunctions import *
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import logging

inputdf_schema = StructType([ \
StructField("battery_level",     LongType(), True), \
StructField("c02_level",   LongType(),   True), \
StructField("cca2",     StringType(),  True), \
StructField("cca3",   StringType(),  True), \
StructField("cn", StringType(),  True), \
StructField("device_id",   LongType(),   True), \
StructField("device_name",   StringType(), True), \
StructField("humidity",   LongType(), True), \
StructField("ip",   StringType(), True), \
StructField("latitude",       DoubleType(),   True), \
StructField("lcd",       StringType(),   True), \
StructField("longitude",       DoubleType(),   True), \
StructField("scale",       StringType(),   True), \
StructField("temp",       LongType(),   True), \
StructField("timestamp",LongType(),True) \
])

input_data = \
[(8,868,"US","USA","United States",1,"meter-gauge-1xbYRYcj",51,"68.161.225.1",38.0,"green",-97.0,"Celsius",34,1458444054093), \
 (7,1473,"NO","NOR","Norway",2,"sensor-pad-2n2Pea",70,"213.161.254.1",62.47,"red",6.15,"Celsius",11,1458444054119), \
 (2,1556,"IT","ITA","Italy",3,"device-mac-36TWSKiT",44,"88.36.5.1",42.83,"red",12.83,"Celsius",19,1458444054120), \
 (6,1080,"US","USA","United States",4,"sensor-pad-4mzWkz",32,"66.39.173.154",44.06,"yellow",-121.32,"Celsius",28,1458444054121), \
 (4,931,"PH","PHL","Philippines",5,"therm-stick-5gimpUrBB",62,"203.82.41.9",14.58,"green",120.97,"Celsius",25,1458444054122), \
 (3,1210,"US","USA","United States",6,"sensor-pad-6al7RTAobR",51,"204.116.105.67",35.93,"yellow",-85.46,"Celsius",27,1458444054122), \
 (3,1129,"CN","CHN","China",7,"meter-gauge-7GeDoanM",26,"220.173.179.1",22.82,"yellow",108.32,"Celsius",18,1458444054123), \
 (0,1536,"JP","JPN","Japan",8,"sensor-pad-8xUD6pzsQI",35,"210.173.177.1",35.69,"red",139.69,"Celsius",27,1458444054123), \
 (3,807,"JP","JPN","Japan",9,"device-mac-9GcjZ2pw",85,"118.23.68.227",35.69,"green",139.69,"Celsius",13,1458444054124), \
 (7,1470,"US","USA","United States",10,"sensor-pad-10BsywSYUF",56,"208.109.163.218",33.61,"red",-111.89,"Celsius",26,1458444054125), \
 (3,1544,"IT","ITA","Italy",11,"meter-gauge-11dlMTZty",85,"88.213.191.34",42.83,"red",12.83,"Celsius",16,1458444054125), \
 (0,1260,"US","USA","United States",12,"sensor-pad-12Y2kIm0o",92,"68.28.91.22",38.0,"yellow",-97.0,"Celsius",12,1458444054126), \
 (6,1007,"IN","IND","India",13,"meter-gauge-13GrojanSGBz",92,"59.144.114.250",28.6,"yellow",77.2,"Celsius",13,1458444054127), \
 (1,1346,"NO","NOR","Norway",14,"sensor-pad-14QL93sBR0j",90,"193.156.90.200",59.95,"yellow",10.75,"Celsius",16,1458444054127), \
 (9,1259,"US","USA","United States",15,"device-mac-15se6mZ",70,"67.185.72.1",47.41,"yellow",-122.0,"Celsius",13,1458444054128), \
 (4,1425,"US","USA","United States",16,"sensor-pad-16aXmIJZtdO",53,"68.85.85.106",38.0,"red",-97.0,"Celsius",15,1458444054128), \
 (0,1466,"US","USA","United States",17,"meter-gauge-17zb8Fghhl",98,"161.188.212.254",39.95,"red",-75.16,"Celsius",31,1458444054129), \
 (4,1096,"CN","CHN","China",18,"sensor-pad-18XULN9Xv",25,"221.3.128.242",25.04,"yellow",102.72,"Celsius",31,1458444054130), \
 (9,1531,"US","USA","United States",19,"meter-gauge-19eg1BpfCO",75,"64.124.180.215",38.0,"red",-97.0,"Celsius",29,1458444054130), \
 (7,1155,"US","USA","United States",20,"sensor-pad-20gFNfBgqr",33,"66.153.162.66",33.94,"yellow",-78.92,"Celsius",10,1458444054131)]


input_df = spark.createDataFrame(data=input_data, schema=inputdf_schema)

transformed_df = transform_data(input_df)


expected_schema = StructType([
            StructField('cn', StringType(), True),
            StructField('TotalDeviceIds', LongType(), False)
            ])

expected_data = [("United States", 10),
                    ("Norway", 2),
                    ("Italy", 2),
                    ("China", 2),
                    ("Japan", 2)]

expected_df = spark.createDataFrame(data=expected_data, schema=expected_schema)


def test_schema():
  assert(expected_df.schema == transformed_df.schema)

def test_df():
  assert sorted(expected_df.collect()) == sorted(transformed_df.collect())

def test_rowcount():
  assert expected_df.count() == 5


