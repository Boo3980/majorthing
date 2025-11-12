from database import get_db
import bcrypt

def login_user(email, password, role):
    db = get_db()

    user = db.execute(
        "SELECT * FROM users WHERE email = ? AND role = ?",
        (email, role)
    ).fetchone()

    if not user:
        return None

    stored_hash = user["password_hash"]

    if bcrypt.checkpw(password.encode(), stored_hash):
        return dict(user)

    return None
