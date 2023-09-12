# Databricks notebook source
# DBTITLE 1,Print out some message
print("Hello from Task C")

# COMMAND ----------

dbutils.widgets.text("top_k", "5")
top_k = int(dbutils.widgets.get("top_k"))
dbutils.widgets.text("top_l", "6")
top_l = int(dbutils.widgets.get("top_l"))

print(top_k, top_l, top_k * top_l)

# COMMAND ----------

# DBTITLE 1,Print out LA local time
from datetime import datetime
import pytz

tz_LA = pytz.timezone("America/Los_Angeles")
datetime_LA = datetime.now(tz_LA)
print("LA time:", datetime_LA.strftime("%Y-%m-%d %H:%M:%S"))

# COMMAND ----------

# DBTITLE 1,%Run get_info
# MAGIC %run ./utilities/get_info

# COMMAND ----------

# DBTITLE 1,Get and print out all variables
(
    username,
    environment,
    notebook_path,
    repo_path,
    catalog,
    landing_path,
    bronze_database,
    silver_database,
    gold_database,
) = get_env_inf()
print(
    f"username: {username}, environment: {environment}, notebook_path: {notebook_path}, repo_path: {repo_path}"
)
print(
    f"catalog: {catalog}, landing_path: {landing_path}, bronze_database: {bronze_database}, silver_database: {silver_database}, gold_database: {gold_database}"
)

# COMMAND ----------

# DBTITLE 1,Print out all variables in SQL
# MAGIC %sql
# MAGIC SELECT "${etl.username}" AS username,
# MAGIC        "${etl.environment}" AS environment,
# MAGIC        "${etl.notebook_path}" AS notebook_path,
# MAGIC        "${etl.repo_path}" AS repo_path,
# MAGIC        "${etl.catalog}" AS `catalog`,
# MAGIC        "${etl.landing_path}" AS landing_path,
# MAGIC        "${etl.bronze_database}" AS bronze_database,
# MAGIC        "${etl.silver_database}" AS silver_database,
# MAGIC        "${etl.gold_database}" AS gold_database

# COMMAND ----------

# DBTITLE 1,Call transform_data function
from dbx_demo_test.tasks.tfmfunctions import *

input_df = spark.read.json("/databricks-datasets/iot/iot_devices.json")
transformed_df = transform_data(input_df)
display(input_df)

# COMMAND ----------

# DBTITLE 1,Display tag.txt
# MAGIC %sh
# MAGIC cat ../tag.txt
