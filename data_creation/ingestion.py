import psycopg
import os
import time

# ============================================================
# CONFIG
# ============================================================

DB_CONFIG = {
    "host": "database-2.cu5iqs8sy3uv.us-east-1.rds.amazonaws.com",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "Sarthak1612",
    "sslmode": "require"
}

CSV_FILE = r"D:\desktop\DatabricksSeries-main\New Project\loans_200k.csv"

TABLE_NAME = "public.loans"


# ============================================================
# CREATE TABLE
# ============================================================

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS public.loans (

    loan_id UUID PRIMARY KEY,
    customer_id UUID,
    loan_application_number VARCHAR(100),

    loan_amount NUMERIC(18,2),
    loan_status VARCHAR(50),

    processing_fee NUMERIC(18,2),
    processing_fee_percentage NUMERIC(8,2),
    total_payable_amount NUMERIC(18,2),

    interest_rate NUMERIC(8,2),
    overdue_interest_rate NUMERIC(8,2),

    loan_tenure VARCHAR(50),
    loan_reason VARCHAR(255),

    is_paid BOOLEAN,
    payment_status VARCHAR(50),

    repay NUMERIC(18,2),
    total_penalty_amount NUMERIC(18,2),
    bounce_amount NUMERIC(18,2),

    waiver_amount NUMERIC(18,2),
    refund_amount NUMERIC(18,2),
    emi_amount NUMERIC(18,2),

    loan_sub_status VARCHAR(100),
    loan_type VARCHAR(100),

    collection_status VARCHAR(100),
    after_disbursal_status VARCHAR(100),
    overdue_sub_status VARCHAR(100),
    sub_status VARCHAR(100),

    is_risky_customer BOOLEAN,
    is_edited BOOLEAN,
    is_in_lms BOOLEAN,
    is_settled BOOLEAN,
    is_audit_done BOOLEAN,
    is_sent_in_mis BOOLEAN,
    is_waived BOOLEAN,
    is_review_done BOOLEAN,
    is_foreclosed BOOLEAN,
    is_bsa_manual BOOLEAN,
    auto_disbursal_checks_passed BOOLEAN,

    disbursed_at TIMESTAMPTZ,
    due_date TIMESTAMPTZ,
    closed_at TIMESTAMPTZ,
    rejected_at TIMESTAMPTZ,
    npa_marked_at TIMESTAMPTZ,
    last_call_date TIMESTAMPTZ,

    loan_officer VARCHAR(150),
    assigned_to VARCHAR(150),
    pre_collection_assignee VARCHAR(150),
    collection_assignee VARCHAR(150),

    rejected_by VARCHAR(150),
    npa_marked_by VARCHAR(150),
    npa_transferred_to VARCHAR(150),
    payment_marked_by VARCHAR(150),

    customer_name VARCHAR(255),
    customer_phone_number VARCHAR(30),

    sanctioned_pdf_key TEXT,
    final_signed_contract TEXT,

    acquisition_source VARCHAR(100),
    application_channel VARCHAR(100),
    platform VARCHAR(50),
    credit_policy VARCHAR(100),
    loan_category VARCHAR(100),

    customer_decile INTEGER,

    ip_address VARCHAR(50),
    user_agent TEXT,

    analyzer_verdict VARCHAR(100),
    bureau_result VARCHAR(100),
    bsa_result VARCHAR(100),

    collection_call_count INTEGER,
    last_call_status VARCHAR(100),

    collection_agency VARCHAR(150),
    call_recording_id VARCHAR(150),

    deviation VARCHAR(20),
    pre_collection_deviation VARCHAR(20),
    collection_deviation VARCHAR(20),

    repayment_schedule JSONB,
    transactions JSONB,
    partial_transactions JSONB,
    emi_dates JSONB,
    loan_logs JSONB,
    email_logs JSONB,
    audit_logs JSONB,
    third_party_data JSONB,
    disbursement_details JSONB,
    edited_loan_details JSONB,
    payment_reminders_sent_at JSONB,
    follow_up JSONB,
    document_information JSONB,
    bank_statement_key JSONB,
    rejection_reason JSONB,
    lending_partner JSONB,
    deviation_details JSONB,
    waiver_details JSONB,
    settlement_details JSONB,
    payment_gateway_orders JSONB,
    disbursement_payment_orders JSONB,

    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ

);
"""


# ============================================================
# LOAD CSV
# ============================================================

def load_csv():

    start_time = time.time()

    print("=" * 60)
    print("POSTGRESQL LOAN DATA INGESTION")
    print("=" * 60)

    print(f"\nCSV File:")
    print(CSV_FILE)

    # --------------------------------------------------------
    # Check CSV exists
    # --------------------------------------------------------

    if not os.path.exists(CSV_FILE):

        raise FileNotFoundError(
            f"CSV file not found:\n{CSV_FILE}"
        )

    file_size = os.path.getsize(CSV_FILE) / (1024 * 1024)

    print(f"CSV Size: {file_size:.2f} MB")

    # --------------------------------------------------------
    # Connect
    # --------------------------------------------------------

    print("\nConnecting to PostgreSQL...")

    with psycopg.connect(**DB_CONFIG) as conn:

        print("✅ Connected to AWS RDS PostgreSQL")

        with conn.cursor() as cur:

            # ------------------------------------------------
            # Create table
            # ------------------------------------------------

            print("\nCreating table...")

            cur.execute(CREATE_TABLE_SQL)

            conn.commit()

            print("✅ Table public.loans created")

            # ------------------------------------------------
            # Load CSV
            # ------------------------------------------------

            print("\nLoading CSV into PostgreSQL...")
            print("Please wait...")

            with open(
                CSV_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                with cur.copy(
                    """
                    COPY public.loans
                    FROM STDIN
                    WITH (
                        FORMAT CSV,
                        HEADER TRUE,
                        NULL ''
                    )
                    """
                ) as copy:

                    while chunk := file.read(1024 * 1024):

                        copy.write(chunk)

            conn.commit()

            # ------------------------------------------------
            # Count rows
            # ------------------------------------------------

            cur.execute(
                "SELECT COUNT(*) FROM public.loans;"
            )

            row_count = cur.fetchone()[0]

            elapsed = time.time() - start_time

            # ------------------------------------------------
            # Result
            # ------------------------------------------------

            print("\n" + "=" * 60)
            print("INGESTION COMPLETE")
            print("=" * 60)

            print(f"Rows loaded : {row_count:,}")
            print(f"Time taken  : {elapsed:.2f} seconds")
            print(f"Table       : public.loans")

            print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:

        load_csv()

    except Exception as e:

        print("\n❌ INGESTION FAILED")
        print("-" * 60)
        print(e)