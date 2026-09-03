# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE loans.gold_data.collection_summary
# MAGIC AS
# MAGIC SELECT
# MAGIC     collection_agency,
# MAGIC     collection_status,
# MAGIC
# MAGIC     COUNT(*) AS loan_count,
# MAGIC
# MAGIC     SUM(amount) AS total_loan_amount,
# MAGIC
# MAGIC     SUM(
# MAGIC         COALESCE(total_amount_paid, 0)
# MAGIC     ) AS total_collected,
# MAGIC
# MAGIC     SUM(
# MAGIC         COALESCE(bounce_amount, 0)
# MAGIC     ) AS total_bounce_amount,
# MAGIC
# MAGIC     SUM(
# MAGIC         COALESCE(total_penalty_amount, 0)
# MAGIC     ) AS total_penalty_amount,
# MAGIC
# MAGIC     SUM(
# MAGIC         COALESCE(waiver_amount, 0)
# MAGIC     ) AS total_waiver_amount,
# MAGIC
# MAGIC     SUM(
# MAGIC         COALESCE(total_payable, 0)
# MAGIC         - COALESCE(total_amount_paid, 0)
# MAGIC     ) AS outstanding_amount
# MAGIC
# MAGIC FROM loans.silver_data.silver_loans
# MAGIC
# MAGIC GROUP BY
# MAGIC     collection_agency,
# MAGIC     collection_status;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from loans.gold_data.collection_summary;