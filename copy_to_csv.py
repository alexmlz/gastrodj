from psycopg2 import connect, sql

try:
    conn = connect(
        host = "localhost",
        dbname = "gastro",
        user = "gastro",
        password = "goethehausffm",
    )
    cursor = conn.cursor()
except Exception as err:
    print("psycopg2 error:", err)
    quit()
else:
    print("connection successful:", conn)
    cursor.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE (table_schema = 'public') ORDER BY table_name;"
    )
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(
            f"COPY {table[0]} TO '/tmp/{table[0]}.csv' "
            f"DELIMITER ',' CSV HEADER;"
        )
        print(f"Finished copying {table[0]}")
