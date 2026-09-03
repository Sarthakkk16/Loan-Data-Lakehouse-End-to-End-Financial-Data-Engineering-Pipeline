# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE loans.gold_data.loan_performance
# MAGIC AS
# MAGIC SELECT
# MAGIC     loan_type,
# MAGIC
# MAGIC     COUNT(*) AS total_loans,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN status = 'Disbursed'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS disbursed_loans,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN status = 'Closed'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS closed_loans,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN status = 'Rejected'
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS rejected_loans,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN marked_npa_at IS NOT NULL
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS npa_loans,
# MAGIC
# MAGIC     SUM(
# MAGIC         CASE
# MAGIC             WHEN is_risky_customer = true
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS risky_loans,
# MAGIC
# MAGIC     SUM(COALESCE(total_amount_paid, 0))
# MAGIC         AS total_repayment,
# MAGIC
# MAGIC     SUM(COALESCE(total_penalty_amount, 0))
# MAGIC         AS total_penalty,
# MAGIC
# MAGIC     SUM(COALESCE(bounce_amount, 0))
# MAGIC         AS total_bounce_amount,
# MAGIC
# MAGIC     SUM(COALESCE(waiver_amount, 0))
# MAGIC         AS total_waiver_amount,
# MAGIC
# MAGIC     SUM(COALESCE(refund_amount, 0))
# MAGIC         AS total_refund_amount,
# MAGIC
# MAGIC     AVG(COALESCE(interest_rate, 0))
# MAGIC         AS avg_interest_rate
# MAGIC
# MAGIC FROM loans.silver_data.silver_loans
# MAGIC
# MAGIC GROUP BY loan_type;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from loans.gold_data.loan_performance;