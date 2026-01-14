FORBIDDEN_SQL = [
    "DELETE", "DROP", "UPDATE", "INSERT",
    "ALTER", "TRUNCATE", "CREATE"
]

def validate_sql(sql: str):
    sql_upper = sql.upper()
    for word in FORBIDDEN_SQL:
        if word in sql_upper:
            raise ValueError("Unsafe SQL operation detected")
