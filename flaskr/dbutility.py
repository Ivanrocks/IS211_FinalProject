import sqlite3


def db_connection():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    return cursor,conn

def authenticate_user(email, password):
    cursor, conn = db_connection()
    user = None
    try:
        # Verify the username and password
        user = cursor.execute(
            "SELECT * FROM authors WHERE email = ? AND password_hash = ?", (email, password)
        ).fetchone()
        conn.commit()
        return user
    except Exception as e:
        print(f"Error matching user password: {e}")
        return False
    finally:
        # Close the connection after the operation
        conn.close()

def get_all_posts():
    cursor, conn = db_connection()
    try:
        blogs = cursor.execute(
            "SELECT * FROM posts"
        ).fetchall()
        return blogs
    except Exception as e:
        print(f"Error retrieving posts: {e}")
        return []
    finally:
        # Close the connection after the operation
        conn.close()
        print("connection closed")