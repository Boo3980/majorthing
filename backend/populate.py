import sqlite3
import bcrypt

# -----------------------------
# 1. LOAD SCHEMA.SQL INTO DB
# -----------------------------
def create_database():
    conn = sqlite3.connect("aims.db")
    with open("schema.sql", "r") as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.close()
    print("[✅] Database created using schema.sql")


# -----------------------------
# 2. GENERATE HASHED PASSWORD
# -----------------------------
def hash_password(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


# -----------------------------
# 3. INSERT DUMMY USERS
# -----------------------------
def insert_dummy_users():
    conn = sqlite3.connect("aims.db")
    cursor = conn.cursor()

    # ONE PASSWORD FOR BOTH USERS
    hashed_pass = hash_password("test123")

    # Insert professor
    cursor.execute("""
        INSERT INTO users (email, password_hash, role)
        VALUES (?, ?, ?)
    """, ("prof1@example.com", hashed_pass, "professor"))

    # Insert student
    cursor.execute("""
        INSERT INTO users (email, password_hash, role)
        VALUES (?, ?, ?)
    """, ("student1@example.com", hashed_pass, "student"))

    conn.commit()
    conn.close()

    print("[✅] Dummy login accounts inserted:")
    print("    prof1@example.com / test123")
    print("    student1@example.com / test123")


# -----------------------------
# 4. INSERT PROFILES (Professor+Student)
# -----------------------------
def insert_profiles():
    conn = sqlite3.connect("aims.db")
    cursor = conn.cursor()

    # Insert a class (prof teaches ONLY one)
    cursor.execute("""
        INSERT INTO classes (class_name, year, professor_id)
        VALUES (?, ?, ?)
    """, ("Computer Science - A", 2024, 1))  # professor_id = 1

    # Insert professor profile
    cursor.execute("""
        INSERT INTO professors (user_id, name, department, class_id)
        VALUES (?, ?, ?, ?)
    """, (1, "Dr. John Fisher", "Computer Science", 1))

    # Insert student profile
    cursor.execute("""
        INSERT INTO students (user_id, name, class_id)
        VALUES (?, ?, ?)
    """, (2, "Alice Green", 1))

    conn.commit()
    conn.close()

    print("[✅] Professor + Student profiles inserted")


# -----------------------------
# 5. RUN EVERYTHING
# -----------------------------
if __name__ == "__main__":
    create_database()
    insert_dummy_users()
    insert_profiles()
    print("\n[✅ ALL DONE] You can now log in with:")
    print("Professor → prof1@example.com / test123")
    print("Student → student1@example.com / test123")
