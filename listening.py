import psycopg2, select, subprocess

conn = psycopg2.connect(dbname="<your_database_name>",
user="postgres",
password="Dhingoo@2001",
host="localhost"
)
conn.set_isolation_level(0)
cur = conn.cursor()
cur.execute("LISTEN schema_changes;")

while True:
    if select.select([conn], [], [], 5) == ([], [], []):
        continue
    conn.poll()
    while conn.notifies:
        conn.notifies.pop()
        subprocess.run(["python3", "generate_erd.py"])  # your SchemaSpy/dbdiagram script
