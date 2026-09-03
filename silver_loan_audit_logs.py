# Create silver_data.silver_loan_audit_logs from raw log JSON columns

from pyspark.sql.functions import col, current_timestamp, lit, explode, from_json
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, TimestampType

# Read the loans table which contains log data as JSON columns
loans_df = spark.table("loans.silver_data.silver_data")

# Define schema for loan_logs JSON
loan_logs_schema = ArrayType(StructType([
    StructField("event", StringType(), True),
    StructField("timestamp", StringType(), True)
]))

# Define schema for audit_logs JSON
audit_logs_schema = ArrayType(StructType([
    StructField("action", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("performed_by", StringType(), True)
]))

# Parse and explode loan_logs column
loan_logs_exploded = loans_df.select(
    col("loan_id"),
    explode(from_json(col("loan_logs"), loan_logs_schema)).alias("log")
).select(
    col("loan_id").cast("STRING").alias("loan_id"),
    col("log.event").cast("STRING").alias("action"),
    lit(None).cast("STRING").alias("performed_by"),
    col("log.timestamp").cast("TIMESTAMP").alias("event_timestamp"),
    lit(None).cast("STRING").alias("event_status"),
    current_timestamp().alias("_processed_at"),
    lit("raw_data_layer.loans.loan_logs").alias("_source_system")
)

# Parse and explode audit_logs column
audit_logs_exploded = loans_df.select(
    col("loan_id"),
    explode(from_json(col("audit_logs"), audit_logs_schema)).alias("log")
).select(
    col("loan_id").cast("STRING").alias("loan_id"),
    col("log.action").cast("STRING").alias("action"),
    col("log.performed_by").cast("STRING").alias("performed_by"),
    col("log.timestamp").cast("TIMESTAMP").alias("event_timestamp"),
    lit(None).cast("STRING").alias("event_status"),
    current_timestamp().alias("_processed_at"),
    lit("raw_data_layer.loans.audit_logs").alias("_source_system")
)

# Union both log sources
silver_loan_audit_logs_df = loan_logs_exploded.unionByName(audit_logs_exploded)

# Write to silver layer table
silver_loan_audit_logs_df.write.mode("overwrite").saveAsTable("loans.silver_data.silver_loan_audit_logs")

print(f"Successfully wrote {silver_loan_audit_logs_df.count()} rows to loans.silver_data.silver_loan_audit_logs")

# Display sample
display(silver_loan_audit_logs_df.limit(100))