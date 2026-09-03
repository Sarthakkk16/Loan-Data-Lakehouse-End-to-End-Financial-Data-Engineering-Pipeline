# Databricks notebook source
# MAGIC %pip install databricks-sdk

# COMMAND ----------

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

w.secrets.put_secret(
    scope="loan-project",
    key="pg_user",
    string_value="postgres"
)

print("pg_user created")

# COMMAND ----------

w.secrets.put_secret(
    scope="loan-project",
    key="pg_password",
    string_value="Sarthak1612"
)

print("pg_password created")

# COMMAND ----------

dbutils.secrets.list("loan-project")

# COMMAND ----------

