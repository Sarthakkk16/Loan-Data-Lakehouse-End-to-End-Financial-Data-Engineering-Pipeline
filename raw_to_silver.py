# Databricks notebook source
# MAGIC %sql
# MAGIC select * from loans.raw_data_layer.loans;

# COMMAND ----------

# MAGIC %md
# MAGIC # Convert all date/time columns from string to timestamp

# COMMAND ----------

from pyspark.sql.functions import col, to_timestamp

df = spark.table("loans.raw_data_layer.loans")

timestamp_columns = [
    "created_at",
    "updated_at",
    "disbursed_at",
    "due_date",
    "closed_at",
    "rejected_at",
    "npa_marked_at",
    "last_call_date"
]

for col_name in timestamp_columns:
    df = df.withColumn(col_name, to_timestamp(col(col_name)))

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Cleaning the tenure column

# COMMAND ----------

from pyspark.sql.functions import regexp_extract

df = df.withColumn("loan_tenure", regexp_extract(col("loan_tenure"), r"(\d+)", 1))

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Standardize categorical columns

# COMMAND ----------

from pyspark.sql.functions import trim, lower, when, col

categorical_columns = {
    "loan_status": "status",
    "payment_status": "payment_status",
    "loan_type": "loan_type",
    "loan_reason": "reason",
    "collection_status": "collection_status",
    "after_disbursal_status": "after_disbursal_status",
    "overdue_substatus": "overdue_substatus",
    "loan_category": "category",
    "acquisition_source": "source",
    "application_channel": "applied_via",
    "platform": "platform",
    "credit_policy": "policy",
    "bureau_result": "bureau_result",
    "bsa_result": "bsa_result"
}

for orig_col, std_col in categorical_columns.items():
    df = df.withColumn(
        std_col,
        when(
            col(orig_col).isNull() | (trim(col(orig_col)) == "") | (lower(trim(col(orig_col))) == "null"),
            None
        ).otherwise(lower(trim(col(orig_col)))
        )
    )

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Status data consistency

# COMMAND ----------

# DBTITLE 1,Cell 9
from pyspark.sql.functions import col, to_timestamp, regexp_extract, trim, lower, when, coalesce, lit

# Reload DataFrame from source to clear stale transformations
df = spark.table("loans.raw_data_layer.loans")

# Reapply timestamp conversions from Cell 3
timestamp_columns = [
    "created_at", "updated_at", "disbursed_at", "due_date",
    "closed_at", "rejected_at", "npa_marked_at", "last_call_date"
]
for col_name in timestamp_columns:
    df = df.withColumn(col_name, to_timestamp(col(col_name)))

# Reapply tenure cleaning from Cell 5
df = df.withColumn("loan_tenure", regexp_extract(col("loan_tenure"), r"(\d+)", 1))

# Reapply categorical standardization from Cell 7
categorical_columns = {
    "loan_status": "status", "payment_status": "payment_status",
    "loan_type": "loan_type", "loan_reason": "reason",
    "collection_status": "collection_status",
    "after_disbursal_status": "after_disbursal_status",
    "overdue_substatus": "overdue_substatus", "loan_category": "category",
    "acquisition_source": "source", "application_channel": "applied_via",
    "platform": "platform", "credit_policy": "policy",
    "bureau_result": "bureau_result", "bsa_result": "bsa_result"
}
for orig_col, std_col in categorical_columns.items():
    df = df.withColumn(
        std_col,
        when(
            col(orig_col).isNull() | (trim(col(orig_col)) == "") | (lower(trim(col(orig_col))) == "null"),
            None
        ).otherwise(lower(trim(col(orig_col))))
    )

# Now apply the status date validation
df = df.withColumn(
    "status_date_valid",
    (
        ((col("loan_status") == "disbursed") & col("disbursed_at").isNotNull()) |
        ((col("loan_status") == "rejected") & col("rejected_at").isNotNull()) |
        ((col("loan_status") == "closed") & col("closed_at").isNotNull() & col("disbursed_at").isNotNull())
    )
)

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Create Loan Age

# COMMAND ----------

from pyspark.sql.functions import datediff, current_date, col

# Calculate loan age in days from created_at to current date
df = df.withColumn("loan_age_days", datediff(current_date(), col("created_at")))

display(df)

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     column_name,
# MAGIC     data_type
# MAGIC FROM loans.information_schema.columns
# MAGIC WHERE table_schema = 'raw_data_layer'
# MAGIC   AND table_name = 'loans'
# MAGIC ORDER BY ordinal_position;

# COMMAND ----------

# MAGIC %md
# MAGIC # Data quality score

# COMMAND ----------

from pyspark.sql.functions import when, col

df = df.withColumn(
    "data_quality_flag",
    when(col("loan_amount") <= 0, 1)
    .when(col("total_payable_amount") < col("loan_amount"), 1)
    .when((col("status") == "disbursed") & col("disbursed_at").isNull(), 1)
    .when(col("updated_at") < col("created_at"), 1)
    .otherwise(0)
)

df.display()

# COMMAND ----------

# Write the transformed data to silver_data table
df.write.mode("overwrite").saveAsTable("loans.silver_data.silver_data")