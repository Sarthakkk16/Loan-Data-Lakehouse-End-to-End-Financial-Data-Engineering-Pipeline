import psycopg

try:
    conn = psycopg.connect(
        host="database-2.cu5iqs8sy3uv.us-east-1.rds.amazonaws.com",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="Sarthak1612"
    )

    print("✅ Connected to AWS RDS PostgreSQL!")

    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]

        print("\nPostgreSQL Version:")
        print(version)

    conn.close()

except Exception as e:
    print("❌ Connection failed!")
    print(e)