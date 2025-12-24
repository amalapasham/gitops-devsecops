from sqlalchemy.orm import Session
from models import Student
from schemas import StudentCreate, StudentUpdate

def create_student(db: Session, student_data: dict):
    db_student = Student(**student_data)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def update_student(db: Session, student_id: int, student_data: dict):
    db_student = get_student_by_id(db, student_id)
    if db_student:
        for key, value in student_data.items():
            if value is not None:
                setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student_by_id(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

def search_students(db: Session, name: str = None, course: str = None):
    query = db.query(Student)
    if name:
        query = query.filter(Student.name.contains(name))
    if course:
        query = query.filter(Student.course.contains(course))
    return query.all()
