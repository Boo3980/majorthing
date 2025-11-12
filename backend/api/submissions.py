from database import get_db

def add_submission(student_id, assignment_id, file_path):
    db = get_db()
    db.execute(
        "INSERT INTO submissions (student_id, assignment_id, file_path) VALUES (?, ?, ?)",
        (student_id, assignment_id, file_path)
    )
    db.commit()

def get_submitted_students(assignment_id):
    db = get_db()
    rows = db.execute(
        "SELECT students.name, submissions.* FROM submissions "
        "JOIN students ON students.student_id = submissions.student_id "
        "WHERE assignment_id = ?",
        (assignment_id,)
    ).fetchall()
    return [dict(r) for r in rows]

def get_not_submitted_students(assignment_id):
    db = get_db()
    rows = db.execute(
        "SELECT name FROM students WHERE student_id NOT IN ("
        "SELECT student_id FROM submissions WHERE assignment_id = ?"
        ")",
        (assignment_id,)
    ).fetchall()
    return [dict(r) for r in rows]
