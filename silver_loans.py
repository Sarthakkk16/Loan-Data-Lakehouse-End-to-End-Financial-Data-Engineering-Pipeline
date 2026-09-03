from pyspark.sql.functions import current_timestamp, lit, col, when

# Select and map columns for silver layer
df = spark.table("loans.silver_data.silver_data")

# Add data quality flag
df = df.withColumn(
    "data_quality_flag",
    when(col("loan_amount") <= 0, 1)
    .when(col("total_payable_amount") < col("loan_amount"), 1)
    .when((col("loan_status") == "disbursed") & col("disbursed_at").isNull(), 1)
    .when(col("updated_at") < col("created_at"), 1)
    .otherwise(0)
)

silver_df = df.select(
    col("loan_seq"),
    col("loan_id"),
    col("customer_id").alias("user_id"),
    col("loan_application_number").alias("application_number"),
    
    col("loan_amount").alias("amount"),
    col("processing_fee").alias("fee"),
    col("processing_fee_percentage").alias("fee_percentage"),
    col("total_payable_amount").alias("total_payable"),
    col("interest_rate"),
    col("overdue_interest_rate").alias("interest_rate_after_due_date"),
    col("emi_amount"),
    col("loan_tenure").alias("tenure_months"),
    
    col("loan_status").alias("status"),
    col("loan_type"),
    col("loan_sub_status"),
    col("sub_status"),
    col("loan_reason").alias("reason"),
    col("payment_status"),
    col("is_paid").alias("paid"),
    
    col("repay").alias("total_amount_paid"),
    col("total_penalty_amount"),
    col("bounce_amount"),
    col("waiver_amount"),
    col("refund_amount"),
    
    col("collection_status"),
    col("after_disbursal_status"),
    col("overdue_substatus"),
    
    col("is_risky_customer"),
    col("loan_category").alias("category"),
    col("customer_decile").alias("decile"),
    
    col("is_edited"),
    col("is_in_lms"),
    col("is_settled").alias("is_settlement"),
    col("is_audit_done"),
    col("is_sent_in_mis"),
    col("is_waived").alias("is_waivered"),
    col("is_review_done"),
    col("is_foreclosed"),
    col("is_bsa_manual"),
    col("auto_disbursal_checks_passed"),
    
    col("acquisition_source").alias("source"),
    col("application_channel").alias("applied_via"),
    col("platform"),
    col("credit_policy").alias("policy"),
    
    col("loan_officer").alias("officer"),
    col("assigned_to"),
    col("pre_collection_assignee").alias("assigned_to_pre_collection"),
    col("collection_assignee").alias("assigned_to_collection"),
    col("collection_agency"),
    
    col("customer_name").alias("user_name"),
    col("customer_phone_number").alias("phone_number"),
    col("ip_address"),
    col("user_agent"),
    
    col("analyzer_verdict").alias("verdict_given_by_analyzer"),
    col("bureau_result"),
    col("bsa_result"),
    
    col("collection_call_count").alias("call_count"),
    col("last_call_status"),
    col("last_call_date"),
    col("call_recording_id").alias("audio_recording_id"),
    
    col("deviation"),
    col("pre_collection_deviation"),
    col("collection_deviation"),
    
    col("created_at"),
    col("updated_at"),
    col("disbursed_at"),
    col("due_date"),
    col("closed_at"),
    col("rejected_at"),
    col("npa_marked_at").alias("marked_npa_at"),
    
    col("rejected_by"),
    col("marked_as_npa_by"),
    col("npa_transferred_to"),
    col("payment_marked_by").alias("mark_as_paid_by"),
    
    when(col("data_quality_flag") == 1, "INVALID").otherwise("VALID").alias("dq_status"),
    col("data_quality_flag").alias("dq_error_count"),
    when(col("data_quality_flag") == 1, "Data quality issues detected").otherwise(None).alias("dq_error_reason"),
    
    current_timestamp().alias("_processed_at"),
    lit("raw_data_layer.loans").alias("_source_system")
)

# Write to silver layer table
silver_df.write.mode("overwrite").saveAsTable("loans.silver_data.silver_loans")

print(f"Successfully wrote {silver_df.count()} rows to loans.silver_data.silver_loans")