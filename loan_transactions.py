# Create silver_data.loan_transactions from raw transaction JSON columns

from pyspark.sql.functions import col, current_timestamp, lit, explode, from_json
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, DecimalType, TimestampType

# Read the loans table which contains transaction data as JSON columns
loans_df = spark.table("loans.raw_data_layer.loans")

# Define schema for transaction JSON based on actual structure
transaction_schema = ArrayType(StructType([
    StructField("transaction_id", StringType(), True),
    StructField("amount", StringType(), True),
    StructField("type", StringType(), True),
    StructField("status", StringType(), True)
]))

# Parse and explode transactions column
transactions_exploded = loans_df.select(
    col("loan_id"),
    explode(from_json(col("transactions"), transaction_schema)).alias("transaction")
).select(
    col("transaction.transaction_id").cast("STRING").alias("transaction_id"),
    col("loan_id").cast("STRING").alias("loan_id"),
    col("transaction.amount").cast("DECIMAL(18,2)").alias("transaction_amount"),
    col("transaction.type").cast("STRING").alias("transaction_type"),
    col("transaction.status").cast("STRING").alias("transaction_status"),
    lit(None).cast("TIMESTAMP").alias("transaction_timestamp"),
    current_timestamp().alias("_processed_at"),
    lit("raw_data_layer.loans.transactions").alias("_source_system")
)

# Parse and explode partial_transactions column
partial_transactions_exploded = loans_df.select(
    col("loan_id"),
    explode(from_json(col("partial_transactions"), transaction_schema)).alias("transaction")
).select(
    col("transaction.transaction_id").cast("STRING").alias("transaction_id"),
    col("loan_id").cast("STRING").alias("loan_id"),
    col("transaction.amount").cast("DECIMAL(18,2)").alias("transaction_amount"),
    col("transaction.type").cast("STRING").alias("transaction_type"),
    col("transaction.status").cast("STRING").alias("transaction_status"),
    lit(None).cast("TIMESTAMP").alias("transaction_timestamp"),
    current_timestamp().alias("_processed_at"),
    lit("raw_data_layer.loans.partial_transactions").alias("_source_system")
)

# Union both transaction sources
silver_transactions_df = transactions_exploded.unionByName(partial_transactions_exploded)

# Write to silver layer table
silver_transactions_df.write.mode("overwrite").saveAsTable("loans.silver_data.silver_loan_transactions")

print(f"Successfully wrote {silver_transactions_df.count()} rows to loans.silver_data.silver_loan_transactions")

# Display sample
display(silver_transactions_df.limit(100))