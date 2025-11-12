from database import get_db
def get_student_professor_id(student_id):
    db = get_db()
    row = db.execute("""
        SELECT professors.prof_id 
        FROM students
        JOIN professors ON students.class_id = professors.class_id
        WHERE students.student_id = ?
    """, (student_id,)).fetchone()
    db.close()
    return row["prof_id"] if row else None


def update_assignment(assignment_id, description):
    db = get_db()
    db.execute(
        "UPDATE assignments SET description = ? WHERE assignment_id = ?",
        (description, assignment_id)
    )
    db.commit()
    db.close()

def get_student_professor_id(student_id):
    db = get_db()
    row = db.execute(
        "SELECT prof_id FROM students WHERE student_id = ?", 
        (student_id,)
    ).fetchone()
    db.close()
    return row["prof_id"] if row else None


def create_assignment(prof_id, title, due_date, description):
    db = get_db()
    db.execute(
        "INSERT INTO assignments (created_by, title, due_date, description) VALUES (?, ?, ?, ?)",
        (prof_id, title, due_date, description)
    )
    db.commit()
    db.close()

def delete_assignment(assignment_id):
    db = get_db()

    db.execute("DELETE FROM submissions WHERE assignment_id = ?", (assignment_id,))
    db.execute("DELETE FROM assignments WHERE assignment_id = ?", (assignment_id,))

    db.commit()
    db.close()



def get_prof_assignments(prof_id):
    db = get_db()
    rows = db.execute(
        "SELECT * FROM assignments WHERE created_by = ?",
        (prof_id,)
    ).fetchall()
    return [dict(r) for r in rows]

