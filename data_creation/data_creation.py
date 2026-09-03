from faker import Faker
import pandas as pd
import numpy as np
import json
import random
import uuid
from datetime import datetime, timedelta, timezone

# ============================================================
# CONFIGURATION
# ============================================================

fake = Faker("en_IN")

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
Faker.seed(SEED)

N = 200_000

OUTPUT_FILE = "loans_200k.csv"

# ============================================================
# MASTER DATA
# ============================================================

STATUSES = [
    "Created",
    "Approved",
    "Disbursed",
    "Rejected",
    "Closed",
    "Cancelled"
]

STATUS_WEIGHTS = [
    0.08,
    0.10,
    0.50,
    0.15,
    0.12,
    0.05
]

PAYMENT_STATUS = [
    "Pending",
    "Paid",
    "Partially Paid",
    "Overdue",
    "Defaulted"
]

LOAN_TYPES = [
    "Personal Loan",
    "Business Loan",
    "Consumer Loan",
    "Education Loan",
    "Medical Loan",
    "Emergency Loan"
]

REASONS = [
    "Personal Expense",
    "Medical Emergency",
    "Home Renovation",
    "Education",
    "Business Expansion",
    "Debt Consolidation",
    "Wedding",
    "Travel",
    "Vehicle Purchase",
    "Emergency"
]

SOURCES = [
    "Google",
    "Facebook",
    "Instagram",
    "Referral",
    "Organic",
    "Affiliate",
    "Partner",
    "WhatsApp"
]

APPLIED_VIA = [
    "Mobile App",
    "Website",
    "Partner App",
    "Branch",
    "Agent"
]

PLATFORMS = [
    "Android",
    "iOS",
    "Web"
]

POLICIES = [
    "Policy_A",
    "Policy_B",
    "Policy_C",
    "Policy_D"
]

CATEGORIES = [
    "Prime",
    "Near Prime",
    "Sub Prime",
    "High Risk"
]

NBFC_LIST = [
    "NBFC_A",
    "NBFC_B",
    "NBFC_C",
    "NBFC_D"
]

OFFICERS = [
    "Rahul Sharma",
    "Amit Verma",
    "Priya Singh",
    "Neha Patel",
    "Rohit Gupta",
    "Ankit Jain",
    "Sneha Mehta",
    "Vikas Kumar"
]

COLLECTION_AGENCIES = [
    "Agency_A",
    "Agency_B",
    "Agency_C",
    "Agency_D"
]

REJECTION_REASONS = [
    "Low Credit Score",
    "Insufficient Income",
    "High FOIR",
    "Bureau Default",
    "Document Mismatch",
    "Bank Statement Issue",
    "Fraud Risk",
    "Policy Deviation",
    "Multiple Applications",
    "Age Criteria",
    "Employment Criteria"
]

VERDICTS = [
    "Approved",
    "Rejected",
    "Manual Review"
]

BUREAU_RESULTS = [
    "Good",
    "Average",
    "Poor",
    "No Hit"
]

BSA_RESULTS = [
    "Pass",
    "Fail",
    "Manual Review"
]

COLLECTION_STATUS = [
    "Not Started",
    "Active",
    "Promise to Pay",
    "Collected",
    "Escalated"
]

AFTER_DISBURSAL_STATUS = [
    "Active",
    "Overdue",
    "Closed",
    "Foreclosed",
    "Settled"
]

OVERDUE_SUBSTATUS = [
    "No Overdue",
    "1-30 DPD",
    "31-60 DPD",
    "61-90 DPD",
    "90+ DPD"
]

# ============================================================
# HELPERS
# ============================================================

def random_datetime(start, end):
    """
    Generate random timezone-aware datetime.
    """

    delta = end - start

    seconds = random.randint(
        0,
        int(delta.total_seconds())
    )

    return start + timedelta(seconds=seconds)


def money(minimum, maximum):
    """
    Generate realistic loan loan_amount.
    Rounded to nearest 100.
    """

    value = random.uniform(minimum, maximum)

    return round(value / 100) * 100


def nullable(value, probability=0.5):
    """
    Return value or None.
    """

    if random.random() < probability:
        return value

    return None


def jsonb_value(value):
    """
    Convert Python dictionary/list into JSON string.

    PostgreSQL JSONB can ingest this value through
    SQLAlchemy/psycopg2.
    """

    return json.dumps(value)


# ============================================================
# USER MASTER
# ============================================================
# Important:
# We create fewer users than loans.
# Therefore multiple loans can belong to the same user.

NUMBER_OF_USERS = 75_000

user_ids = [
    str(uuid.uuid4())
    for _ in range(NUMBER_OF_USERS)
]

user_names = [
    fake.name()
    for _ in range(NUMBER_OF_USERS)
]

phone_numbers = [
    fake.msisdn()
    for _ in range(NUMBER_OF_USERS)
]

# ============================================================
# DATE RANGE
# ============================================================

START_DATE = datetime(
    2024, 1, 1, tzinfo=timezone.utc
)

END_DATE = datetime(
    2026, 8, 31, 23, 59, 59, tzinfo=timezone.utc
)

# ============================================================
# GENERATE LOANS
# ============================================================

rows = []

for i in range(N):

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    user_index = random.randint(
        0,
        NUMBER_OF_USERS - 1
    )

    customer_id = user_ids[user_index]
    customer_name = user_names[user_index]
    phone = phone_numbers[user_index]

    # --------------------------------------------------------
    # APPLICATION
    # --------------------------------------------------------

    loan_id = str(uuid.uuid4())

    loan_application_number = (
        f"LN{2024 + (i % 3)}"
        f"{i + 1:08d}"
    )

    # --------------------------------------------------------
    # CREATED DATE
    # --------------------------------------------------------

    created_at = random_datetime(
        START_DATE,
        END_DATE
    )

    updated_at = created_at + timedelta(
        hours=random.randint(1, 720)
    )

    # Don't allow updated_at beyond current generation date
    if updated_at > END_DATE:
        updated_at = END_DATE

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    loan_status = np.random.choice(
        STATUSES,
        p=STATUS_WEIGHTS
    )

    # --------------------------------------------------------
    # LOAN AMOUNT
    # --------------------------------------------------------

    loan_amount = money(
        5_000,
        1_000_000
    )

    # --------------------------------------------------------
    # LOAN TERMS
    # --------------------------------------------------------

    tenure_months = random.choice([
        3, 6, 9, 12, 18, 24, 36, 48
    ])

    loan_tenure = f"{tenure_months} Months"

    interest_rate = round(
        random.uniform(10, 28),
        2
    )

    overdue_interest_rate = round(
        interest_rate + random.uniform(4, 12),
        2
    )

    # --------------------------------------------------------
    # FEES
    # --------------------------------------------------------

    processing_fee_percentage = round(
        random.uniform(1, 5),
        2
    )

    processing_fee = round(
        loan_amount * processing_fee_percentage / 100,
        2
    )

    # Approximate interest
    interest_amount = round(
        loan_amount
        * interest_rate
        / 100
        * tenure_months
        / 12,
        2
    )

    total_payable_amount = round(
        loan_amount
        + interest_amount
        + processing_fee,
        2
    )

    emi_amount = round(
        total_payable_amount / tenure_months,
        2
    )

    # --------------------------------------------------------
    # APPROVAL / DISBURSEMENT
    # --------------------------------------------------------

    disbursed_at = None
    rejected_at = None
    closed_at = None
    due_date = None
    npa_marked_at = None

    if loan_status in [
        "Approved",
        "Disbursed",
        "Closed"
    ]:

        if loan_status in [
            "Disbursed",
            "Closed"
        ]:

            disbursed_at = created_at + timedelta(
                days=random.randint(1, 10)
            )

            due_date = disbursed_at + timedelta(
                days=tenure_months * 30
            )

        if loan_status == "Closed":

            closed_at = disbursed_at + timedelta(
                days=random.randint(
                    30,
                    tenure_months * 30
                )
            )

    elif loan_status == "Rejected":

        rejected_at = created_at + timedelta(
            hours=random.randint(1, 72)
        )

    # --------------------------------------------------------
    # PAYMENT
    # --------------------------------------------------------

    if loan_status == "Closed":

        is_paid = True

        payment_status = "Paid"

        repay = total_payable_amount

        total_penalty_amount = 0

        bounce_amount = 0

    elif loan_status == "Disbursed":

        payment_status = random.choice([
            "Pending",
            "Partially Paid",
            "Overdue",
            "Defaulted"
        ])

        if payment_status == "Pending":

            is_paid = False

            repay = 0

            total_penalty_amount = 0

            bounce_amount = 0

        elif payment_status == "Partially Paid":

            is_paid = False

            repay = round(
                random.uniform(
                    0.1,
                    0.7
                ) * total_payable_amount,
                2
            )

            total_penalty_amount = round(
                random.uniform(0, 10_000),
                2
            )

            bounce_amount = round(
                random.uniform(0, 5_000),
                2
            )

        elif payment_status == "Overdue":

            is_paid = False

            repay = round(
                random.uniform(
                    0,
                    0.6
                ) * total_payable_amount,
                2
            )

            total_penalty_amount = round(
                random.uniform(500, 15_000),
                2
            )

            bounce_amount = round(
                random.uniform(500, 5_000),
                2
            )

        else:

            is_paid = False

            repay = round(
                random.uniform(
                    0,
                    0.3
                ) * total_payable_amount,
                2
            )

            total_penalty_amount = round(
                random.uniform(
                    1_000,
                    25_000
                ),
                2
            )

            bounce_amount = round(
                random.uniform(
                    1_000,
                    10_000
                ),
                2
            )

    else:

        is_paid = False

        payment_status = "Pending"

        repay = 0

        total_penalty_amount = 0

        bounce_amount = 0

    # --------------------------------------------------------
    # REFUND / WAIVER
    # --------------------------------------------------------

    refund_amount = round(
        random.uniform(0, 5_000),
        2
    ) if random.random() < 0.05 else 0

    waiver_amount = round(
        random.uniform(0, 10_000),
        2
    ) if random.random() < 0.08 else 0

    # --------------------------------------------------------
    # SUB STATUS
    # --------------------------------------------------------

    if loan_status == "Rejected":

        loan_sub_status = "Rejected"

        sub_status = "Rejected"

    elif loan_status == "Closed":

        loan_sub_status = random.choice([
            "Closed",
            "ReLoan",
            "Foreclosed",
            "Settled"
        ])

        sub_status = loan_sub_status

    elif loan_status == "Disbursed":

        loan_sub_status = random.choice([
            "Active",
            "Overdue",
            "ReLoan"
        ])

        sub_status = loan_sub_status

    else:

        loan_sub_status = loan_status

        sub_status = loan_status

    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    risk_probability = random.random()

    is_risky_customer = (
        risk_probability < 0.20
    )

    customer_decile = random.randint(1, 10)

    if customer_decile <= 3:
        loan_category = "Prime"

    elif customer_decile <= 6:
        loan_category = "Near Prime"

    elif customer_decile <= 8:
        loan_category = "Sub Prime"

    else:
        loan_category = "High Risk"

    # --------------------------------------------------------
    # COLLECTION
    # --------------------------------------------------------

    if loan_status == "Disbursed":

        collection_status = random.choice(
            COLLECTION_STATUS
        )

        after_disbursal_status = random.choice(
            AFTER_DISBURSAL_STATUS
        )

        overdue_substatus = random.choice(
            OVERDUE_SUBSTATUS
        )

    elif loan_status == "Closed":

        collection_status = "Collected"

        after_disbursal_status = "Closed"

        overdue_substatus = "No Overdue"

    else:

        collection_status = "Not Started"

        after_disbursal_status = None

        overdue_substatus = "No Overdue"

    # --------------------------------------------------------
    # NPA
    # --------------------------------------------------------

    if (
        loan_status == "Disbursed"
        and overdue_substatus in [
            "61-90 DPD",
            "90+ DPD"
        ]
    ):

        npa_marked_at = (
            disbursed_at
            + timedelta(
                days=random.randint(
                    90,
                    180
                )
            )
        )

    # --------------------------------------------------------
    # ASSIGNMENT
    # --------------------------------------------------------

    loan_officer = random.choice(OFFICERS)

    assigned_to = loan_officer

    pre_collection_assignee = nullable(
        random.choice(OFFICERS),
        0.7
    )

    collection_assignee = nullable(
        random.choice(OFFICERS),
        0.6
    )

    # --------------------------------------------------------
    # REJECTION
    # --------------------------------------------------------

    if loan_status == "Rejected":

        rejected_by = random.choice(
            OFFICERS
        )

        rejection_reason = {
            "code": f"REJ{random.randint(100,999)}",
            "loan_reason": random.choice(
                REJECTION_REASONS
            ),
            "severity": random.choice([
                "Low",
                "Medium",
                "High"
            ])
        }

    else:

        rejected_by = None

        rejection_reason = None

    # --------------------------------------------------------
    # VERDICT / BUREAU
    # --------------------------------------------------------

    analyzer_verdict = random.choice(
        VERDICTS
    )

    bureau_result = random.choice(
        BUREAU_RESULTS
    )

    bsa_result = random.choice(
        BSA_RESULTS
    )

    # --------------------------------------------------------
    # CALLS
    # --------------------------------------------------------

    collection_call_count = random.randint(0, 20)

    last_call_status = (
        random.choice([
            "Connected",
            "Not Connected",
            "Promise to Pay",
            "Busy",
            "Wrong Number"
        ])
        if collection_call_count > 0
        else None
    )

    last_call_date = (
        created_at + timedelta(
            days=random.randint(1, 30)
        )
        if collection_call_count > 0
        else None
    )

    # --------------------------------------------------------
    # JSONB DATA
    # --------------------------------------------------------

    repayment_schedule = [
        {
            "emi_no": emi,
            "loan_amount": round(
                emi_amount,
                2
            ),
            "loan_status": random.choice([
                "Paid",
                "Pending",
                "Overdue"
            ])
        }
        for emi in range(
            1,
            min(tenure_months, 6) + 1
        )
    ]

    transactions = [
        {
            "transaction_id": str(
                uuid.uuid4()
            ),
            "loan_amount": round(
                random.uniform(
                    500,
                    emi_amount
                ),
                2
            ),
            "type": "PAYMENT",
            "loan_status": "SUCCESS"
        }
    ] if repay > 0 else []

    partial_transactions = []

    if payment_status == "Partially Paid":

        partial_transactions = [
            {
                "transaction_id": str(
                    uuid.uuid4()
                ),
                "loan_amount": round(
                    repay,
                    2
                ),
                "loan_status": "PARTIAL"
            }
        ]

    emi_dates = [
        (
            disbursed_at
            + timedelta(days=30 * x)
        ).isoformat()
        for x in range(
            1,
            min(tenure_months, 6) + 1
        )
    ] if disbursed_at else []

    loan_logs = [
        {
            "event": "APPLICATION_CREATED",
            "timestamp": created_at.isoformat()
        }
    ]

    if disbursed_at:

        loan_logs.append({
            "event": "LOAN_DISBURSED",
            "timestamp": disbursed_at.isoformat()
        })

    email_logs = [
        {
            "type": "LOAN_APPLICATION",
            "loan_status": random.choice([
                "SENT",
                "DELIVERED"
            ])
        }
    ]

    audit_logs = [
        {
            "action": "LOAN_CREATED",
            "performed_by": loan_officer,
            "timestamp": created_at.isoformat()
        }
    ]

    third_party_data = {
        "bureau_score": random.randint(
            500,
            850
        ),
        "income_verified": random.choice([
            True,
            False
        ]),
        "employment_verified": random.choice([
            True,
            False
        ])
    }

    disbursement_details = (
        {
            "bank_name": random.choice([
                "HDFC Bank",
                "ICICI Bank",
                "Axis Bank",
                "SBI",
                "Kotak Bank"
            ]),
            "utr": fake.bothify(
                text="UTR##################"
            ),
            "loan_status": "SUCCESS"
        }
        if disbursed_at
        else None
    )

    edited_loan_details = (
        {
            "edited": True,
            "edited_by": loan_officer,
            "loan_reason": "Manual Correction"
        }
        if random.random() < 0.05
        else None
    )

    payment_reminders_sent_at = [
        (
            created_at
            + timedelta(days=random.randint(1, 30))
        ).isoformat()
        for _ in range(
            random.randint(0, 3)
        )
    ]

    follow_up = {
        "required": random.choice([
            True,
            False
        ]),
        "next_follow_up": (
            created_at
            + timedelta(days=random.randint(1, 15))
        ).date().isoformat()
    }

    document_information = {
        "aadhaar": "verified",
        "pan": "verified",
        "bank_statement": random.choice([
            "verified",
            "pending",
            "rejected"
        ])
    }

    bank_statement_key = {
        "provider": random.choice([
            "Perfios",
            "Finbox",
            "Decentro"
        ]),
        "loan_status": random.choice([
            "SUCCESS",
            "PENDING",
            "FAILED"
        ])
    }

    lending_partner = {
        "name": random.choice(
            NBFC_LIST
        ),
        "application_id": (
            f"NBFC{random.randint(100000,999999)}"
        )
    }

    deviation_details = (
        {
            "type": random.choice([
                "Income Deviation",
                "Tenure Deviation",
                "Policy Deviation"
            ]),
            "severity": random.choice([
                "Low",
                "Medium",
                "High"
            ])
        }
        if random.random() < 0.10
        else None
    )

    waiver_details = (
        {
            "waiver_type": random.choice([
                "Penalty Waiver",
                "Interest Waiver",
                "Fee Waiver"
            ]),
            "loan_amount": waiver_amount
        }
        if waiver_amount > 0
        else None
    )

    settlement_details = (
        {
            "settlement_amount": round(
                total_payable_amount * random.uniform(
                    0.5,
                    0.9
                ),
                2
            ),
            "loan_status": "SETTLED"
        }
        if sub_status == "Settled"
        else None
    )

    payment_gateway_orders = {
        "order_id": f"PG_{uuid.uuid4().hex[:16]}",
        "loan_status": random.choice([
            "SUCCESS",
            "PENDING",
            "FAILED"
        ])
    }

    disbursement_payment_orders = (
        {
            "order_id": (
                f"DISB_{uuid.uuid4().hex[:16]}"
            ),
            "loan_status": "SUCCESS"
        }
        if disbursed_at
        else None
    )

    # --------------------------------------------------------
    # MISCELLANEOUS
    # --------------------------------------------------------

    deviation = (
        "Yes"
        if deviation_details
        else "No"
    )

    pre_collection_deviation = random.choice([
        "Yes",
        "No"
    ])

    collection_deviation = random.choice([
        "Yes",
        "No"
    ])

    is_edited = random.random() < 0.05
    is_in_lms = loan_status in [
        "Approved",
        "Disbursed",
        "Closed"
    ]

    is_settled = (
        sub_status == "Settled"
    )

    is_audit_done = random.random() < 0.85

    is_sent_in_mis = random.random() < 0.90

    is_waived = waiver_amount > 0

    is_review_done = random.random() < 0.80

    is_foreclosed = (
        sub_status == "Foreclosed"
    )

    is_bsa_manual = (
        bsa_result == "Manual Review"
    )

    auto_disbursal_checks_passed = (
        loan_status in [
            "Disbursed",
            "Closed"
        ]
    )

    # --------------------------------------------------------
    # OTHER TEXT FIELDS
    # --------------------------------------------------------

    acquisition_source = random.choice(SOURCES)

    application_channel = random.choice(
        APPLIED_VIA
    )

    platform = random.choice(
        PLATFORMS
    )

    credit_policy = random.choice(
        POLICIES
    )

    ip_address = fake.ipv4()

    user_agent = fake.user_agent()

    call_recording_id = (
        f"AUD_{uuid.uuid4().hex[:16]}"
        if collection_call_count > 0
        else None
    )

    # --------------------------------------------------------
    # CREATE RECORD
    # --------------------------------------------------------

    row = {

        "id": loan_id,

        "customer_id": customer_id,

        "loan_application_number":
            loan_application_number,

        "loan_amount":
            loan_amount,

        "loan_status":
            loan_status,

        "processing_fee":
            processing_fee,

        "processing_fee_percentage":
            processing_fee_percentage,

        "total_payable_amount":
            total_payable_amount,

        "interest_rate":
            interest_rate,

        "overdue_interest_rate":
            overdue_interest_rate,

        "loan_tenure":
            loan_tenure,

        "loan_reason":
            random.choice(REASONS),

        "is_paid":
            is_paid,

        "payment_status":
            payment_status,

        "repay":
            repay,

        "total_penalty_amount":
            total_penalty_amount,

        "bounce_amount":
            bounce_amount,

        "waiver_amount":
            waiver_amount,

        "refund_amount":
            refund_amount,

        "emi_amount":
            emi_amount,

        "loan_sub_status":
            loan_sub_status,

        "loan_type":
            random.choice(LOAN_TYPES),

        "collection_status":
            collection_status,

        "after_disbursal_status":
            after_disbursal_status,

        "overdue_substatus":
            overdue_substatus,

        "sub_status":
            sub_status,

        "is_risky_customer":
            is_risky_customer,

        "is_edited":
            is_edited,

        "is_in_lms":
            is_in_lms,

        "is_settled":
            is_settled,

        "is_audit_done":
            is_audit_done,

        "is_sent_in_mis":
            is_sent_in_mis,

        "is_waived":
            is_waived,

        "is_review_done":
            is_review_done,

        "is_foreclosed":
            is_foreclosed,

        "is_bsa_manual":
            is_bsa_manual,

        "auto_disbursal_checks_passed":
            auto_disbursal_checks_passed,

        "disbursed_at":
            disbursed_at,

        "due_date":
            due_date,

        "closed_at":
            closed_at,

        "rejected_at":
            rejected_at,

        "npa_marked_at":
            npa_marked_at,

        "last_call_date":
            last_call_date,

        "loan_officer":
            loan_officer,

        "assigned_to":
            assigned_to,

        "pre_collection_assignee":
            pre_collection_assignee,

        "collection_assignee":
            collection_assignee,

        "rejected_by":
            rejected_by,

        "npa_marked_by":
            nullable(
                random.choice(OFFICERS),
                0.3
            ) if npa_marked_at else None,

        "npa_transferred_to":
            nullable(
                random.choice(OFFICERS),
                0.3
            ) if npa_marked_at else None,

        "payment_marked_by":
            nullable(
                random.choice(OFFICERS),
                0.7
            ) if is_paid else None,

        "customer_name":
            customer_name,

        "customer_phone_number":
            phone,

        "sanctioned_pdf_key":
            nullable(
                f"s3://loans/sanctioned/{loan_id}.pdf",
                0.7
            ),

        "final_signed_contract":
            nullable(
                f"s3://loans/contracts/{loan_id}.pdf",
                0.7
            ),

        "acquisition_source":
            acquisition_source,

        "application_channel":
            application_channel,

        "platform":
            platform,

        "credit_policy":
            credit_policy,

        "loan_category":
            loan_category,

        "customer_decile":
            customer_decile,

        "ip_address":
            ip_address,

        "user_agent":
            user_agent,

        "analyzer_verdict":
            analyzer_verdict,

        "bureau_result":
            bureau_result,

        "bsa_result":
            bsa_result,

        "collection_call_count":
            collection_call_count,

        "last_call_status":
            last_call_status,

        "collection_agency":
            nullable(
                random.choice(
                    COLLECTION_AGENCIES
                ),
                0.5
            ),

        "call_recording_id":
            call_recording_id,

        "deviation":
            deviation,

        "pre_collection_deviation":
            pre_collection_deviation,

        "collection_deviation":
            collection_deviation,

        "repayment_schedule":
            jsonb_value(
                repayment_schedule
            ),

        "transactions":
            jsonb_value(
                transactions
            ),

        "partial_transactions":
            jsonb_value(
                partial_transactions
            ),

        "emi_dates":
            jsonb_value(
                emi_dates
            ),

        "loan_logs":
            jsonb_value(
                loan_logs
            ),

        "email_logs":
            jsonb_value(
                email_logs
            ),

        "audit_logs":
            jsonb_value(
                audit_logs
            ),

        "third_party_data":
            jsonb_value(
                third_party_data
            ),

        "disbursement_details":
            jsonb_value(
                disbursement_details
            ) if disbursement_details else None,

        "edited_loan_details":
            jsonb_value(
                edited_loan_details
            ) if edited_loan_details else None,

        "payment_reminders_sent_at":
            jsonb_value(
                payment_reminders_sent_at
            ),

        "follow_up":
            jsonb_value(
                follow_up
            ),

        "document_information":
            jsonb_value(
                document_information
            ),

        "bank_statement_key":
            jsonb_value(
                bank_statement_key
            ),

        "rejection_reason":
            jsonb_value(
                rejection_reason
            ) if rejection_reason else None,

        "lending_partner":
            jsonb_value(
                lending_partner
            ),

        "deviation_details":
            jsonb_value(
                deviation_details
            ) if deviation_details else None,

        "waiver_details":
            jsonb_value(
                waiver_details
            ) if waiver_details else None,

        "settlement_details":
            jsonb_value(
                settlement_details
            ) if settlement_details else None,

        "payment_gateway_orders":
            jsonb_value(
                payment_gateway_orders
            ),

        "disbursement_payment_orders":
            jsonb_value(
                disbursement_payment_orders
            ) if disbursement_payment_orders else None,

        "created_at":
            created_at,

        "updated_at":
            updated_at
    }

    rows.append(row)

# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(rows)

# ============================================================
# COLUMN ORDER
# ============================================================

columns = [
    "id",
    "customer_id",
    "loan_application_number",
    "loan_amount",
    "loan_status",
    "processing_fee",
    "processing_fee_percentage",
    "total_payable_amount",
    "interest_rate",
    "overdue_interest_rate",
    "loan_tenure",
    "loan_reason",
    "is_paid",
    "payment_status",
    "repay",
    "total_penalty_amount",
    "bounce_amount",
    "waiver_amount",
    "refund_amount",
    "emi_amount",
    "loan_sub_status",
    "loan_type",
    "collection_status",
    "after_disbursal_status",
    "overdue_substatus",
    "sub_status",
    "is_risky_customer",
    "is_edited",
    "is_in_lms",
    "is_settled",
    "is_audit_done",
    "is_sent_in_mis",
    "is_waived",
    "is_review_done",
    "is_foreclosed",
    "is_bsa_manual",
    "auto_disbursal_checks_passed",
    "disbursed_at",
    "due_date",
    "closed_at",
    "rejected_at",
    "npa_marked_at",
    "last_call_date",
    "loan_officer",
    "assigned_to",
    "pre_collection_assignee",
    "collection_assignee",
    "rejected_by",
    "npa_marked_by",
    "npa_transferred_to",
    "payment_marked_by",
    "customer_name",
    "customer_phone_number",
    "sanctioned_pdf_key",
    "final_signed_contract",
    "acquisition_source",
    "application_channel",
    "platform",
    "credit_policy",
    "loan_category",
    "customer_decile",
    "ip_address",
    "user_agent",
    "analyzer_verdict",
    "bureau_result",
    "bsa_result",
    "collection_call_count",
    "last_call_status",
    "collection_agency",
    "call_recording_id",
    "deviation",
    "pre_collection_deviation",
    "collection_deviation",
    "repayment_schedule",
    "transactions",
    "partial_transactions",
    "emi_dates",
    "loan_logs",
    "email_logs",
    "audit_logs",
    "third_party_data",
    "disbursement_details",
    "edited_loan_details",
    "payment_reminders_sent_at",
    "follow_up",
    "document_information",
    "bank_statement_key",
    "rejection_reason",
    "lending_partner",
    "deviation_details",
    "waiver_details",
    "settlement_details",
    "payment_gateway_orders",
    "disbursement_payment_orders",
    "created_at",
    "updated_at"
]

df = df[columns]

# ============================================================
# EXPORT CSV
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ============================================================
# VALIDATION
# ============================================================

print("=" * 60)
print("DATA GENERATION COMPLETE")
print("=" * 60)

print(f"Rows       : {len(df):,}")
print(f"Columns    : {len(df.columns)}")
print(f"Output     : {OUTPUT_FILE}")

print("\nSTATUS DISTRIBUTION")
print(df["loan_status"].value_counts())

print("\nPAYMENT STATUS")
print(df["payment_status"].value_counts())

print("\nLOAN TYPE")
print(df["loan_type"].value_counts())

print("\nDATA TYPES")
print(df.dtypes)

print("\nFIRST 5 RECORDS")
print(df.head())

