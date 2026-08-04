import psycopg2
import subprocess

conn = psycopg2.connect(dbname="<your_db_name>", user="<your_username>", password="<your_password>", host="<your_hostname>") #postgres details
cur = conn.cursor()

cur.execute("""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = '<your_schema_name>'
    ORDER BY table_name, ordinal_position;
""")
columns = cur.fetchall()

cur.execute("""
    SELECT
        tc.table_name, kcu.column_name,
        ccu.table_name AS foreign_table, ccu.column_name AS foreign_column
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage ccu
        ON tc.constraint_name = ccu.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = '<your_schema_name>';
""")
fks = cur.fetchall()

tables = {}
for table, col, dtype in columns:
    tables.setdefault(table, []).append((col, dtype))

type_map = {
    "timestamp without time zone": "timestamp",
    "character varying": "varchar",
}

with open("/home/chaitalithkkr/erd.mmd", "w") as f:
    f.write("erDiagram\n")
    for src, col, ftable, fcol in fks:
        f.write(f"    {ftable} ||--o{{ {src} : \"{fcol}\"\n")
    for table, cols in tables.items():
        f.write(f"    {table} {{\n")
        for col, dtype in cols:
            short_dtype = type_map.get(dtype, dtype).replace(' ', '_')
            f.write(f"        {short_dtype} {col}\n")
        f.write("    }\n")
print("erd.mmd written.")

#update file locations as necessary
result = subprocess.run(
    ["mmdc", "-i", "/home/erd.mmd", "-o", "/home/rd.svg",
     "-p", "/home/puppeteer-config.json",  
     "-c", "/home/mermaid-config.json"],
    capture_output=True, text=True
)

print(result.stdout)
print(result.stderr)
print("erd.svg rendered.")
