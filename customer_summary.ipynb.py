# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE loans.gold_data.customer_summary
# MAGIC AS
# MAGIC SELECT
# MAGIC     user_id,
# MAGIC
# MAGIC     COUNT(*) AS total_loans,
# MAGIC
# MAGIC     SUM(amount) AS total_loan_amount,
# MAGIC
# MAGIC     SUM(
# MAGIC         amount - COALESCE(fee, 0)
# MAGIC     ) AS total_net_disbursed,
# MAGIC
# MAGIC     SUM(
# MAGIC         COALESCE(total_amount_paid, 0)
# MAGIC     ) AS total_amount_paid,
# MAGIC
# MAGIC     SUM(
# MAGIC         COALESCE(total_payable, 0)
# MAGIC         - COALESCE(total_amount_paid, 0)
# MAGIC     ) AS total_outstanding,
# MAGIC
# MAGIC     AVG(amount) AS average_loan_amount,
# MAGIC
# MAGIC     AVG(interest_rate) AS average_interest_rate,
# MAGIC
# MAGIC     MAX(
# MAGIC         CASE
# MAGIC             WHEN is_risky_customer = true
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS is_risky_customer,
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
# MAGIC             WHEN marked_npa_at IS NOT NULL
# MAGIC             THEN 1
# MAGIC             ELSE 0
# MAGIC         END
# MAGIC     ) AS npa_loans,
# MAGIC
# MAGIC     MAX(created_at) AS latest_loan_application,
# MAGIC
# MAGIC     MAX(disbursed_at) AS latest_disbursement
# MAGIC
# MAGIC FROM loans.silver_data.silver_loans
# MAGIC
# MAGIC GROUP BY user_id;