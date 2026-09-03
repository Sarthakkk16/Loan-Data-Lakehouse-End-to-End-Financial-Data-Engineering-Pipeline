from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# --------------------------------------------------
# PostgreSQL connection
# --------------------------------------------------

pg_host = "database-2.cu5iqs8sy3uv.us-east-1.rds.amazonaws.com"
pg_port = "5432"
pg_database = "postgres"

pg_user = dbutils.secrets.get(
    scope="loan-project",
    key="pg_user"
)

pg_password = dbutils.secrets.get(
    scope="loan-project",
    key="pg_password"
)


# --------------------------------------------------
# Gold tables
# --------------------------------------------------

gold_tables = {
    "loan_portfolio_summary":
        "loans.gold_data.loan_portfolio_summary",

    "loan_performance":
        "loans.gold_data.loan_performance",

    "customer_summary":
        "loans.gold_data.customer_summary",

    "collection_summary":
        "loans.gold_data.collection_summary"
}


# --------------------------------------------------
# Write Gold → PostgreSQL
# --------------------------------------------------

for target_table, source_table in gold_tables.items():

    print(
        f"Loading {source_table} "
        f"→ gold_loans.{target_table}"
    )

    # Read Gold table from Databricks
    df = spark.table(source_table)

    # Write to PostgreSQL using Serverless PostgreSQL connector
    (
        df.write
        .format("postgresql")
        .option("host", pg_host)
        .option("port", pg_port)
        .option("database", pg_database)
        .option("dbtable", f"gold_loans.{target_table}")
        .option("user", pg_user)
        .option("password", pg_password)
        .option("batchsize", "1000")
        .mode("overwrite")
        .save()
    )

    print(
        f"Successfully loaded "
        f"gold_loans.{target_table}"
    )