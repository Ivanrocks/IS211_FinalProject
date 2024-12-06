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

def create_post(postContent, title, user_id):
    cursor, conn = db_connection()

    try:
        conn.execute(
            'INSERT INTO posts(title, content, status, published_date, user_id) VALUES (?, ?, "draft", CURRENT_TIMESTAMP, ?)',
            (title,postContent, user_id))
        conn.commit()
        print("Post created: " ,cursor.lastrowid)
        return True
    except Exception as e:
        print(f"Error creating Post: {e}" )
        return False
    finally:
        conn.close()

def get_all_posts_by_user(user_id):
    cursor, conn = db_connection()
    try:
        posts = cursor.execute(
            "SELECT * FROM posts WHERE user_id is ? ORDER BY published_date ASC",
            (user_id,)
        ).fetchall()
        conn.commit()
        return posts
    except Exception as e:
        print(f"Error fetching Post: {e}" )
        return []
    finally:
        conn.close()



def get_all_posts():
    cursor, conn = db_connection()
    try:
        blogs = cursor.execute(
            "SELECT * FROM posts WHERE status is 'published' ORDER BY published_date DESC"
        ).fetchall()
        return blogs
    except Exception as e:
        print(f"Error retrieving posts: {e}")
        return []
    finally:
        # Close the connection after the operation
        conn.close()
        print("connection closed")

def publish_post(post_id):
    cursor, conn = db_connection()
    try:
        conn.execute(
            'UPDATE posts SET status = "published" WHERE post_id = ?',
            (post_id,)
        )
        conn.commit()
        print("Post updated: ")
        return True
    except Exception as e:
        print(f"Error retrieving posts: {e}")
        return False
    finally:
        # Close the connection after the operation
        conn.close()
        print("connection closed")

def unpublish_post(post_id):
    cursor, conn = db_connection()
    try:
        conn.execute(
            'UPDATE posts SET status = "draft" WHERE post_id = ?',
            (post_id,)
        )
        conn.commit()
        print("Post updated: ")
        return True
    except Exception as e:
        print(f"Error retrieving posts: {e}")
        return False
    finally:
        # Close the connection after the operation
        conn.close()
        print("connection closed")

def delete_post(post_id):
    cursor, conn = db_connection()
    try:
        conn.execute(
            'DELETE FROM posts WHERE post_id = ?',
            (post_id,)
        )
        conn.commit()
        print("Post Deleted: ")
        return True
    except Exception as e:
        print(f"Error retrieving posts: {e}")
        return False
    finally:
        # Close the connection after the operation
        conn.close()
        print("connection closed")

def get_post(post_id):
    cursor, conn = db_connection()
    try:
        post = cursor.execute(
            'SELECT * FROM posts WHERE post_id = ?',
            (post_id,)
        ).fetchone()
        conn.commit()
        print("Post Fetched: ")
        return post
    except Exception as e:
        print(f"Error retrieving posts: {e}")
        return None
    finally:
        # Close the connection after the operation
        conn.close()
        print("connection closed")

def update_post(post_id, title, content):
    cursor, conn = db_connection()
    try:
        conn.execute(
            'UPDATE posts SET title = ?, content = ? WHERE post_id = ?',
            (title,content,post_id)
        )
        conn.commit()
        print("Post updated: ")
        return True
    except Exception as e:
        print(f"Error retrieving posts: {e}")
        return False
    finally:
        # Close the connection after the operation
        conn.close()
        print("connection closed")