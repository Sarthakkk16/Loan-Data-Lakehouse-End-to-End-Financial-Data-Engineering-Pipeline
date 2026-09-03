# Databricks notebook source
# MAGIC %sql
# MAGIC select * from loans.silver_data.silver_loans;

# COMMAND ----------

# DBTITLE 1,Cell 2
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE loans.gold_data.loan_portfolio_summary AS
# MAGIC SELECT
# MAGIC   status,
# MAGIC   loan_type,
# MAGIC   category,
# MAGIC   COUNT(*) as total_loans,
# MAGIC   SUM(amount) as total_amount,
# MAGIC   AVG(amount) as avg_amount,
# MAGIC   SUM(total_payable) as total_payable_amount,
# MAGIC   AVG(interest_rate) as avg_interest_rate,
# MAGIC   SUM(total_payable - total_amount_paid) as total_outstanding,
# MAGIC   SUM(CASE WHEN payment_status = 'overdue' THEN total_payable - total_amount_paid ELSE 0 END) as total_overdue
# MAGIC FROM loans.silver_data.silver_loans
# MAGIC GROUP BY status, loan_type, category

# COMMAND ----------

# DBTITLE 1,View loan portfolio summary
# MAGIC %sql
# MAGIC SELECT * FROM loans.gold_data.loan_portfolio_summary
# MAGIC ORDER BY total_loans DESC

# COMMAND ----------

