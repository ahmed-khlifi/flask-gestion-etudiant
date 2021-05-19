import sqlite3

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("gestion.sqlite3")
    except sqlite3.error as e:
        print(e)
    return conn