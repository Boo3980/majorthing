from backend.database import get_db

def add_todo(student_id, content):
    db = get_db()
    db.execute(
        "INSERT INTO todo_items (student_id, content) VALUES (?, ?)",
        (student_id, content)
    )
    db.commit()

def get_todos(student_id):
    db = get_db()
    rows = db.execute(
        "SELECT * FROM todo_items WHERE student_id = ?",
        (student_id,)
    ).fetchall()
    return [dict(r) for r in rows]
