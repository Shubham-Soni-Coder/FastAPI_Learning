import sqlite3


def conn_database(query: str, parameter=None):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    if parameter:
        cursor.execute(query, parameter)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def normalize(name: str) -> str:
    return " ".join(name.strip().split())
