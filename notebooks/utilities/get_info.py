# Databricks notebook source
import os
import sys
import json


def parse_user(user_name):
    """Module to parse out users email and return a defined string as a variable"""
    act_user = user_name.split("@")
    return "_".join(act_user[0].split("."))


def get_env_inf():
    ####========================================================
    ### Get username
    ####========================================================
    # username = parse_user(spark.sql("SELECT current_user()").first()[0])
    username = parse_user(
        dbutils.notebook.entry_point.getDbutils()
        .notebook()
        .getContext()
        .userName()
        .get()
    )

    ####========================================================
    ### Get environment, notebook_path, repo_path
    ####========================================================
    # api_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().getOrElse(None)+"/api/"
    # api_token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
    notebook_path = (
        dbutils.notebook.entry_point.getDbutils()
        .notebook()
        .getContext()
        .notebookPath()
        .get()
    )
    repo_path = "/".join(notebook_path.split("/")[:4])
    environment = repo_path.split("/")[2]

    ####========================================================
    ### Get Catalog, Landing_Path, Databases
    ####========================================================
    env_json = f"/Workspace{repo_path}/conf/setup/environments.json"

    f = open(env_json)
    data = json.load(f)
    for item in data:
        if item["Environment"] == environment:
            catalog = item["Catalog"]
            landing_path = item["Landing_Path"]
            bronze_database = item["Bronze_Database"]
            silver_database = item["Silver_Database"]
            gold_database = item["Gold_Database"]
            break

    ####========================================================
    ### Set variables at SQL
    ### username, environment, notebook_path, repo_path,
    ### catalog, landing_path, bronze_database, silver_database, gold_database
    ####========================================================
    var_dict = {
        "username": username,
        "environment": environment,
        "notebook_path": notebook_path,
        "repo_path": repo_path,
        "catalog": catalog,
        "landing_path": landing_path,
        "bronze_database": bronze_database,
        "silver_database": silver_database,
        "gold_database": gold_database,
    }
    for key, value in var_dict.items():
        spark.sql(f"SET etl.{key} = {value}")

    ####========================================================
    ### return
    ### username, environment, notebook_path, repo_path,
    ### catalog, landing_path, bronze_database, silver_database, gold_database
    ####========================================================
    return (
        username,
        environment,
        notebook_path,
        repo_path,
        catalog,
        landing_path,
        bronze_database,
        silver_database,
        gold_database,
    )

# COMMAND ----------

# (
#     username,
#     environment,
#     notebook_path,
#     repo_path,
#     catalog,
#     landing_path,
#     bronze_database,
#     silver_database,
#     gold_database,
# ) = get_env_inf()
# print(
#     f"username: {username}, environment: {environment}, notebook_path: {notebook_path}, repo_path: {repo_path}"
# )
# print(
#     f"catalog: {catalog}, landing_path: {landing_path}, bronze_database: {bronze_database}, silver_database: {silver_database}, gold_database: {gold_database}"
# )

# COMMAND ----------

# %sql
# SELECT "${etl.username}" AS username,
#        "${etl.environment}" AS environment,
#        "${etl.notebook_path}" AS notebook_path,
#        "${etl.repo_path}" AS repo_path,
#        "${etl.catalog}" AS `catalog`,
#        "${etl.landing_path}" AS landing_path,
#        "${etl.bronze_database}" AS bronze_database,
#        "${etl.silver_database}" AS silver_database,
#        "${etl.gold_database}" AS gold_database

# COMMAND ----------

# import os
# import sys
# import json
# import requests


# def parse_user(user_name):
#     """Module to parse out users email and return a defined string as a variable"""
#     act_user = user_name.split("@")
#     return "_".join(act_user[0].split("."))


# def get_env_inf():
#     ####========================================================
#     ### Get username
#     ####========================================================
#     # username = parse_user(
#     #     dbutils.notebook.entry_point.getDbutils()
#     #     .notebook()
#     #     .getContext()
#     #     .tags()
#     #     .apply("user")
#     # )
#     username = parse_user(spark.sql("SELECT current_user()").first()[0])

#     ####========================================================
#     ### Get notebook, repo_data
#     ####========================================================
#     ctx = json.loads(
#         dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
#     )

#     notebook_path = ctx["extraContext"]["notebook_path"]
#     repo_path = "/".join(notebook_path.split("/")[:4])
#     api_url = ctx["extraContext"]["api_url"]
#     api_token = ctx["extraContext"]["api_token"]

#     repo_dir_data = requests.get(
#         f"{api_url}/api/2.0/workspace/get-status",
#         headers={"Authorization": f"Bearer {api_token}"},
#         json={"path": repo_path},
#     ).json()
#     repo_id = repo_dir_data["object_id"]
#     repo_data = requests.get(
#         f"{api_url}/api/2.0/repos/{repo_id}",
#         headers={"Authorization": f"Bearer {api_token}"},
#     ).json()
#     environment = repo_data["path"].split("/")[2]
#     repo_path = repo_data["path"]
#     if "branch" in repo_data:
#         repo_branch = repo_data["branch"]
#     else:
#         repo_branch = repo_data["head_commit_id"][:7]

#     ####========================================================
#     ### Get Catalog, Landing_Path, Databases
#     ####========================================================
#     if environment == "Development":
#         env_json = f"/Workspace/Repos/{environment}/dbx-demo-test-{repo_branch}/conf/setup/environments.json"
#     else:
#         env_json = (
#             f"/Workspace/Repos/{environment}/dbx-demo-test/conf/setup/environments.json"
#         )

#     f = open(env_json)
#     data = json.load(f)
#     for item in data:
#         if item["Environment"] == environment:
#             catalog = item["Catalog"]
#             landing_path = item["Landing_Path"]
#             bronze_database = item["Bronze_Database"]
#             silver_database = item["Silver_Database"]
#             gold_database = item["Gold_Database"]
#             break

#     ####========================================================
#     ### return
#     ### username, environment, notebook_path, repo_path, repo_branch,
#     ### catalog, landing_path, bronze_database, silver_database, gold_database
#     ####========================================================
#     var_dict = {
#         "username": username,
#         "environment": environment,
#         "notebook_path": notebook_path,
#         "repo_path": repo_path,
#         "repo_branch": repo_branch,
#         "catalog": catalog,
#         "landing_path": landing_path,
#         "bronze_database": bronze_database,
#         "silver_database": silver_database,
#         "gold_database": gold_database,
#     }
#     for key, value in var_dict.items():
#         spark.sql(f"SET etl.{key} = {value}")

#     ####========================================================
#     ### return
#     ### username, environment, notebook_path, repo_path, repo_branch,
#     ### catalog, landing_path, bronze_database, silver_database, gold_database
#     ####========================================================
#     return (
#         username,
#         environment,
#         notebook_path,
#         repo_path,
#         repo_branch,
#         catalog,
#         landing_path,
#         bronze_database,
#         silver_database,
#         gold_database,
#     )

# COMMAND ----------

# username, environment, notebook_path, repo_path, repo_branch, catalog, landing_path, bronze_database, silver_database, gold_database = get_env_inf()
# print(f"username: {username}, environment: {environment}, notebook_path: {notebook_path}, repo_path: {repo_path}, repo_branch: {repo_branch}")
# print(f"catalog: {catalog}, landing_path: {landing_path}, bronze_database: {bronze_database}, silver_database: {silver_database}, gold_database: {gold_database}")

# COMMAND ----------

# env_json = "/Workspace/Repos/Production/dbx-demo-test/conf/setup/environments.json"
# f = open(env_json)
# data = json.load(f)
# for item in data:
#     if item['Environment'] == 'Production':
#         Catalog = item['Catalog']
#         Landing_Path = item['Landing_Path']
#         Bronze_Database = item['Bronze_Database']
#         Silver_Database = item['Silver_Database']
#         Gold_Database = item['Gold_Database']
#         break

# print(Catalog, Landing_Path, Bronze_Database, Silver_Database, Gold_Database)

# COMMAND ----------

# import pytest
# import os
# import sys

# # Run all tests in the repository root.
# notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
# repo_root = os.path.dirname(os.path.dirname(notebook_path))
# # os.chdir(f'/Workspace/{repo_root}')

# print(f"notebook_path: {notebook_path}")
# print(f"path: {repo_root}")
# print(f"Environment: {repo_root.split('/')[2]}")

# COMMAND ----------

# import json
# import requests

# ctx = json.loads(
#   dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())

# notebook_path = ctx['extraContext']['notebook_path']
# repo_path = '/'.join(notebook_path.split('/')[:4])
# api_url = ctx['extraContext']['api_url']
# api_token = ctx['extraContext']['api_token']

# repo_dir_data = requests.get(f"{api_url}/api/2.0/workspace/get-status",
#                              headers = {"Authorization": f"Bearer {api_token}"},
#                              json={"path": repo_path}).json()
# repo_id = repo_dir_data['object_id']
# repo_data = requests.get(f"{api_url}/api/2.0/repos/{repo_id}",
#                          headers = {"Authorization": f"Bearer {api_token}"}
#                         ).json()

# if 'branch' in repo_data:
#     branch =  repo_data['branch']
# else:
#     branch = repo_data['head_commit_id'][:7]

# print(f"Environment: {repo_data['path'].split('/')[2]}")
# print(f"path: {repo_data['path']}")
# print(f"branch: {branch}")
