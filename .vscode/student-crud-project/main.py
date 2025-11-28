from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Student Management System", version="1.0")

# SQLite connection
def get_db():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            standard INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class StudentCreate(BaseModel):
    name: str
    age: int
    standard: int

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Student Management System",
        "version": "1.0",
        "endpoints": {
            "create_student": "POST /students/",
            "get_students": "GET /students/", 
            "get_by_class": "GET /students/standard/{standard}",
            "update_student": "PUT /students/{student_id}",
            "delete_student": "DELETE /students/{standard}?student_name=NAME"
        }
    }

# CREATE Student
@app.post("/students/")
def create_student(student: StudentCreate):
    if student.standard not in range(1, 11):  # 1 to 10
        raise HTTPException(status_code=400, detail="Standard must be between 1 and 10")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, standard) VALUES (?, ?, ?)",
        (student.name, student.age, student.standard)
    )
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    
    return {"id": student_id, "message": "Student created successfully", "student": student.dict()}

# GET All Students
@app.get("/students/")
def get_all_students():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return {"students": [dict(student) for student in students]}

# GET Students by Class
@app.get("/students/standard/{standard}")
def get_students_by_class(standard: int):
    if standard not in range(1, 11):  # 1 to 10
        raise HTTPException(status_code=400, detail="Standard must be between 1 and 10")
    
    conn = get_db()
    students = conn.execute(
        "SELECT * FROM students WHERE standard = ?", 
        (standard,)
    ).fetchall()
    conn.close()
    
    return {"standard": standard, "students": [dict(student) for student in students]}

# UPDATE Student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate):
    if student.standard not in range(1, 11):  # 1 to 10
        raise HTTPException(status_code=400, detail="Standard must be between 1 and 10")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name = ?, age = ?, standard = ? WHERE id = ?",
        (student.name, student.age, student.standard, student_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    
    if updated == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {"message": "Student updated successfully"}

# DELETE Student
@app.delete("/students/{standard}")
def delete_student(standard: int, student_name: str = Query(...)):
    if standard not in range(1, 11):  # 1 to 10
        raise HTTPException(status_code=400, detail="Standard must be between 1 and 10")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM students WHERE standard = ? AND name = ?",
        (standard, student_name)
    )
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Student not found in this class")
    
    return {"message": f"Student {student_name} from Standard {standard} deleted successfully"}