def is_safe_query(query):
    dangerous = ["DROP", "DELETE", "UPDATE", "ALTER", "INSERT"]

    for word in dangerous:
        if word in query.upper():
            return False

    return True
