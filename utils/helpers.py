def is_safe_query(query):
    dangerous = ["DROP", "DELETE", "UPDATE", "ALTER", "INSERT"]

    query_upper = query.upper()

    for word in dangerous:
        if word in query_upper:
            return False

    return query_upper.strip().startswith("SELECT")

def extract_tables(schema):
    tables = []
    for line in schema.split("\n"):
        if line.startswith("Table:"):
            table_name = line.split("(")[0].replace("Table:", "").strip()
            tables.append(table_name)
    return tables


def is_valid_table(sql, schema):
    tables = extract_tables(schema)

    sql_lower = sql.lower()

    for table in tables:
        if table.lower() in sql_lower:
            return True

    return False
