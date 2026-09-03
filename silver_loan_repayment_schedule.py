# Create silver_data.silver_loan_repayment_schedule from raw JSON columns

from pyspark.sql.functions import col, current_timestamp, lit, explode, from_json, posexplode
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, DecimalType, TimestampType

# Read the loans table which contains repayment schedule data as JSON columns
loans_df = spark.table("loans.silver_data.silver_data")

# Define schema for repayment_schedule JSON
repayment_schedule_schema = ArrayType(StructType([
    StructField("amount", StringType(), True),
    StructField("status", StringType(), True)
]))

# Define schema for emi_dates JSON
emi_dates_schema = ArrayType(StringType())

# Parse and explode repayment_schedule column with position
repayment_exploded = loans_df.select(
    col("loan_id"),
    posexplode(from_json(col("repayment_schedule"), repayment_schedule_schema)).alias("emi_no", "schedule")
).select(
    col("loan_id").cast("STRING").alias("loan_id"),
    (col("emi_no") + 1).alias("emi_no"),  # 1-based EMI number
    col("schedule.amount").cast("DECIMAL(18,2)").alias("emi_amount"),
    col("schedule.status").cast("STRING").alias("emi_status")
)

# Parse and explode emi_dates column with position
emi_dates_exploded = loans_df.select(
    col("loan_id"),
    posexplode(from_json(col("emi_dates"), emi_dates_schema)).alias("emi_no", "date")
).select(
    col("loan_id").cast("STRING").alias("loan_id"),
    (col("emi_no") + 1).alias("emi_no"),  # 1-based EMI number
    col("date").cast("TIMESTAMP").alias("emi_date")
)

# Join both sources on loan_id and emi_no
silver_repayment_df = repayment_exploded.join(
    emi_dates_exploded,
    on=["loan_id", "emi_no"],
    how="full_outer"
).select(
    col("loan_id"),
    col("emi_no"),
    col("emi_amount"),
    col("emi_status"),
    col("emi_date"),
    current_timestamp().alias("_processed_at"),
    lit("raw_data_layer.loans").alias("_source_system")
)

# Write to silver layer table
silver_repayment_df.write.mode("overwrite").saveAsTable("loans.silver_data.silver_loan_repayment_schedule")

print(f"Successfully wrote {silver_repayment_df.count()} rows to loans.silver_data.silver_loan_repayment_schedule")

# Display sample
display(silver_repayment_df.limit(100))