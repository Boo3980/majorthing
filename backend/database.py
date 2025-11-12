import sqlite3

DB_PATH = "aims.db"  # if db sits inside same backend folder

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def save_active_user(user_id, role):
    db = get_db()
    db.execute("DELETE FROM active_user")  # always keep only one active user
    db.execute("INSERT INTO active_user (user_id, role) VALUES (?, ?)",
               (user_id, role))
    db.commit()
    db.close()


def get_active_user():
    db = get_db()
    row = db.execute("SELECT user_id, role FROM active_user LIMIT 1").fetchone()
    db.close()
    if row:
        return {"user_id": row["user_id"], "role": row["role"]}
    return {"user_id": None, "role": None}
