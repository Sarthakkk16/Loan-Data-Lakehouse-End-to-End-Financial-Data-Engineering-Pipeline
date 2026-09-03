# Create silver_data.silver_loan_collection from raw loans table

from pyspark.sql.functions import col, current_timestamp, lit

# Read the loans table
loans_df = spark.table("loans.silver_data.silver_data")

# Create silver_loan_collection table
silver_loan_collection_df = loans_df.select(
    col("loan_id").cast("STRING").alias("loan_id"),
    
    col("collection_status").cast("STRING").alias("collection_status"),
    col("collection_agency").cast("STRING").alias("collection_agency"),
    col("collection_assignee").cast("STRING").alias("assigned_to_collection"),
    
    col("pre_collection_assignee").cast("STRING").alias("assigned_to_pre_collection"),
    
    col("pre_collection_deviation").cast("STRING").alias("pre_collection_deviation"),
    col("collection_deviation").cast("STRING").alias("collection_deviation"),
    
    col("collection_call_count").cast("INT").alias("call_count"),
    col("last_call_status").cast("STRING").alias("last_call_status"),
    col("last_call_date").cast("TIMESTAMP").alias("last_call_date"),
    col("call_recording_id").cast("STRING").alias("audio_recording_id"),
    
    current_timestamp().alias("_processed_at"),
    lit("raw_data_layer.loans").alias("_source_system")
)

# Write to silver layer table
silver_loan_collection_df.write.mode("overwrite").saveAsTable("loans.silver_data.silver_loan_collection")

print(f"Successfully wrote {silver_loan_collection_df.count()} rows to loans.silver_data.silver_loan_collection")

# Display sample
display(silver_loan_collection_df.limit(100))