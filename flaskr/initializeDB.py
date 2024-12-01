import sqlite3
def db_connection():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    return cursor,conn

def create_database():

    cursor,conn = db_connection()
    with open('schema.sql', 'r') as file:
        schema = file.read()
        cursor.executescript(schema)
    # Commit changes and close the connection
    conn.commit()
    conn.close()