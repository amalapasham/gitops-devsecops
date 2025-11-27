from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Student Management System")

# Temporary database with 9 students - FIXED
students_db = [
    {"id": 1, "name": "Amala", "age": 22, "course": "Computer Science"},
    {"id": 2, "name": "Raju", "age": 25, "course": "Mathematics"},
    {"id": 3, "name": "Priya", "age": 21, "course": "Physics"},
    {"id": 4, "name": "Kiran", "age": 23, "course": "Chemistry"},
    {"id": 5, "name": "Sneha", "age": 24, "course": "Biology"},
    {"id": 6, "name": "Vikram", "age": 26, "course": "Engineering"},
    {"id": 7, "name": "Anjali", "age": 20, "course": "Commerce"},
    {"id": 8, "name": "Suresh", "age": 27, "course": "Business"},
    {"id": 9, "name": "Rithik", "age": 8, "course": "2nd standard"}  # ✅ FIXED
]

# ✅ AUTOMATIC ID GENERATION SYSTEM
current_id = 10  # Next student ki ID 10 start (9 varaku already undi)

class Student(BaseModel):
    name: str
    age: int
    course: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None

# 🏠 HOME ROUTE
@app.get("/")
def home():
    return {"message": "Student Management System"}

# ➕ CREATE STUDENT - AUTOMATIC ID
@app.post("/students/")
def create_student(student: Student):
    global current_id
    
    student_data = {
        "id": current_id,
        "name": student.name,
        "age": student.age,
        "course": student.course
    }
    
    students_db.append(student_data)
    current_id += 1
    
    return {
        "message": "Student created successfully!",
        "student": student_data,
        "next_available_id": current_id
    }

# 📖 READ ALL STUDENTS
@app.get("/students/")
def read_all_students():
    return {
        "total_students": len(students_db),
        "students": students_db
    }

# 🔍 READ SINGLE STUDENT
@app.get("/students/{student_id}")
def read_student(student_id: int):
    for student in students_db:
        if student["id"] == student_id:
            return {
                "message": "Student found!",
                "student": student
            }
    return {"error": "Student not found!"}

# ✏️ UPDATE STUDENT
@app.put("/students/{student_id}")
def update_student(student_id: int, student_update: StudentUpdate):
    for student in students_db:
        if student["id"] == student_id:
            if student_update.name is not None:
                student["name"] = student_update.name
            if student_update.age is not None:
                student["age"] = student_update.age
            if student_update.course is not None:
                student["course"] = student_update.course
            
            return {
                "message": "Student updated successfully!",
                "updated_student": student
            }
    
    return {"error": "Student not found!"}

# 🗑️ DELETE STUDENT
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i, student in enumerate(students_db):
        if student["id"] == student_id:
            deleted_student = students_db.pop(i)
            return {
                "message": "Student deleted successfully!",
                "deleted_student": deleted_student
            }
    
    return {"error": "Student not found!"}

# Server run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)