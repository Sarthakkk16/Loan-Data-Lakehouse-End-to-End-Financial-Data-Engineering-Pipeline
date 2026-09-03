from pyspark import pipelines as dp
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

# Bronze layer: Read from PostgreSQL using JDBC batch reads
@dp.materialized_view(
    name="loans_snapshot",
    comment="Snapshot of loans data from PostgreSQL with UUID columns cast to STRING"
)
def loans_snapshot():
    # Read from PostgreSQL using JDBC format with batch read
    # The connection parameter references the pg_to_catalog connection
    df = (
        spark.read
        .format("postgresql")
        .option("connection", "pg_to_catalog")
        .option("dbtable", "public.loans")
        .load()
    )
    
    # Cast all UUID columns to STRING to avoid PostgreSQL UUID function errors
    # This handles columns like loan_id, customer_id that are UUID type in PostgreSQL
    uuid_columns = ["loan_id", "customer_id"]
    
    for col_name in uuid_columns:
        if col_name in df.columns:
            df = df.withColumn(col_name, F.col(col_name).cast(StringType()))
    
    return df

# Create target streaming table for CDC
dp.create_streaming_table(
    name="loans",
    comment="Target table for loans data with SCD Type 1 (latest values only)",
    cluster_by_auto=True
)

# Apply SCD Type 1 CDC from snapshot to target
dp.create_auto_cdc_from_snapshot_flow(
    target="loans",
    source="loans_snapshot",
    keys=["loan_id"],
    stored_as_scd_type=1
)