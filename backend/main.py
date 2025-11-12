from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.assignments import delete_assignment, get_prof_assignments, create_assignment, update_assignment
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import get_db, save_active_user, get_active_user
import bcrypt
from api.assignments import get_prof_assignments, get_student_professor_id



app = FastAPI()
print("FASTAPI LOADED FROM THIS main.py")


@app.get("/student/{student_id}/assignments")
def get_student_assignments(student_id: int):
    prof_id = get_student_professor_id(student_id)

    if not prof_id:
        return {"success": False, "message": "No professor assigned to this student."}

    return get_prof_assignments(prof_id)

@app.get("/student/{student_id}/assignments")
def get_assignments_for_student(student_id: int):
    prof_id = get_student_professor_id(student_id)
    assignments = get_prof_assignments(prof_id)
    return assignments


@app.get("/active")
def active_user():
    return get_active_user()

# -----------------------------------------------------------------
# 👇 1. ADD THE MISSING LOGIN ROUTE
# -----------------------------------------------------------------
@app.post("/login")
async def login_user(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    db = get_db()
    user_row = db.execute(
        "SELECT user_id, password_hash FROM users WHERE email = ? AND role = ?",
        (email, role)
    ).fetchone()

    if not user_row:
        return {"success": False, "message": "Invalid credentials."}

    # Check the password
    hashed_pass = user_row["password_hash"].encode('utf-8')
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_pass):
        return {"success": False, "message": "Invalid credentials."}

    # Password is correct. Get the correct ID.
    user_id = user_row["user_id"]
    
    # This is the crucial part.
    # We must return the PROF_ID from the 'professors' table,
    # not the USER_ID from the 'users' table.
    if role == "professor":
        prof_row = db.execute(
            "SELECT prof_id FROM professors WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        
        if not prof_row:
             db.close()
             return {"success": False, "message": "Professor profile not found."}
        
        # This is the ID your frontend needs
        id_to_return = prof_row["prof_id"]

    else: # role == "student"
        # (You would do the same for student_id here)
        # For now, just return user_id for students
        id_to_return = user_id

    db.close()
    
    save_active_user(user_id, role) 
    return {"success": True, "role": role, "user_id": id_to_return}


# -----------------------------------------------------------------
# 👇 2. ADD THE MISSING "GET ASSIGNMENTS" ROUTE
# -----------------------------------------------------------------
@app.get("/prof/{prof_id}/assignments")
def get_assignments_route(prof_id: int):
    # This function is from your assignments.py file
    assignments = get_prof_assignments(prof_id)
    return assignments

# -----------------------------------------------------------------
# (Your other routes)
# -----------------------------------------------------------------

@app.put("/assignment/{assignment_id}")
async def update_assignment_route(assignment_id: int, request: Request):
    data = await request.json()
    description = data.get("description")
    update_assignment(assignment_id, description)
    return {"success": True}

@app.post("/prof/{prof_id}/assignments")
async def create_assignment_route(prof_id: int, request: Request):
    data = await request.json()
    title = data.get("title")
    due_date = data.get("due_date")
    description = data.get("description")
    create_assignment(prof_id, title, due_date, description)
    return {"success": True}

@app.delete("/assignment/{assignment_id}")
def delete_assignment_route(assignment_id: int):
    delete_assignment(assignment_id)
    return {"success": True}

# ✅ ENABLE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ SIMPLE TEST ROUTE
@app.get("/")
def home():
    return {"hello": "world"}
print("FASTAPI LOADED FROM THIS main.py")

@app.put("/assignment/{assignment_id}")
async def update_assignment_route(assignment_id: int, request: Request):
    data = await request.json()
    description = data.get("description")

    update_assignment(assignment_id, description)
    return {"success": True}


@app.post("/prof/{prof_id}/assignments")
async def create_assignment_route(prof_id: int, request: Request):
    data = await request.json()
    title = data.get("title")
    due_date = data.get("due_date")
    description = data.get("description")

    create_assignment(prof_id, title, due_date, description)
    return {"success": True}


@app.delete("/assignment/{assignment_id}")
def delete_assignment_route(assignment_id: int):
    delete_assignment(assignment_id)
    return {"success": True}


# ✅ ENABLE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ SIMPLE TEST ROUTE
@app.get("/")
def home():
    return {"status": "ok"}

# ✅ LOGIN ROUTE (POST)
@app.post("/login")
def login(data: dict):
    print("✅ /login endpoint HIT with:", data)
    return {"success": True, "role": data.get("role")}

@app.get("/prof/{prof_id}/assignments")
def get_professor_assignments(prof_id: int):
    return get_prof_assignments(prof_id)


def save_active_user(user_id, role):
    db = get_db()
    db.execute("DELETE FROM active_user")
    db.execute("INSERT INTO active_user (user_id, role) VALUES (?,?)", (user_id, role))
    db.commit()
    db.close()

@app.get("/active")
def get_active_user():
    db = get_db()
    row = db.execute("SELECT user_id, role FROM active_user LIMIT 1").fetchone()
    if row:
        return {"user_id": row["user_id"], "role": row["role"]}
    return {"user_id": None, "role": None}
