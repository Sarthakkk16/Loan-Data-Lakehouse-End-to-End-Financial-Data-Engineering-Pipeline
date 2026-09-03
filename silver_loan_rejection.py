# Create silver_data.silver_loan_rejection from raw loans table

from pyspark.sql.functions import col, current_timestamp, lit, when, regexp_extract

# Read the loans table
loans_df = spark.table("loans.silver_data.silver_data")

# Filter for rejected loans only
rejected_loans_df = loans_df.filter(col("rejected_at").isNotNull())

# Create silver_loan_rejection table
silver_loan_rejection_df = rejected_loans_df.select(
    col("loan_id").cast("STRING").alias("loan_id"),
    
    # Extract rejection code from rejection_reason (assuming format like "CODE: reason")
    regexp_extract(col("rejection_reason"), r"^([A-Z0-9_]+):", 1).alias("rejection_code"),
    
    col("rejection_reason").cast("STRING").alias("rejection_reason"),
    
    # Derive rejection severity based on rejection reason keywords
    when(
        col("rejection_reason").rlike("(?i)(fraud|identity|suspicious|blacklist)"), "HIGH"
    ).when(
        col("rejection_reason").rlike("(?i)(income|credit|score|eligibility|policy)"), "MEDIUM"
    ).when(
        col("rejection_reason").rlike("(?i)(incomplete|document|verification)"), "LOW"
    ).otherwise("UNKNOWN").alias("rejection_severity"),
    
    col("rejected_by").cast("STRING").alias("rejected_by"),
    col("rejected_at").cast("TIMESTAMP").alias("rejected_at"),
    
    current_timestamp().alias("_processed_at"),
    lit("raw_data_layer.loans").alias("_source_system")
)

# Write to silver layer table
silver_loan_rejection_df.write.mode("overwrite").saveAsTable("loans.silver_data.silver_loan_rejection")

print(f"Successfully wrote {silver_loan_rejection_df.count()} rows to loans.silver_data.silver_loan_rejection")

# Display sample
display(silver_loan_rejection_df.limit(100))