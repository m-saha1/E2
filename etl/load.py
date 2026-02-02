import psycopg2


def load_data(records):
    print("[LOAD] Writing to PostgreSQL")

    conn = psycopg2.connect(
        host="localhost",
        database="ons_housing",
        user="postgres",
        password="Cover5987"
    )

    cur = conn.cursor()

    for r in records:
        cur.execute(
            """
            INSERT INTO housing_data (dataset_id, geography, year, value)
            VALUES (%s, %s, %s, %s)
            """,
            (r["dataset_id"], r["geography"], r["year"], r["value"])
        )

    conn.commit()
    cur.close()
    conn.close()

    print("[LOAD] Data committed successfully")

