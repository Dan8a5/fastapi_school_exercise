# Import necessary modules
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, select
import uvicorn
# Import database-related functions from db.py
from db import init_db, get_session

# Create a FastAPI application instance
app = FastAPI()

# Model Definitions
# These classes define both the database schema and the API data models

class StudentBase(SQLModel):
    # Base model for Student, containing common attributes
    name: str

class Student(StudentBase, table=True):
    # Student model for database table, inherits from StudentBase
    # The id field is optional (can be None) and is set as the primary key
    id: Optional[int] = Field(default=None, primary_key=True)

class CourseBase(SQLModel):
    # Base model for Course, containing common attributes
    name: str

class Course(CourseBase, table=True):
    # Course model for database table, inherits from CourseBase
    id: Optional[int] = Field(default=None, primary_key=True)

class EnrollmentBase(SQLModel):
    # Base model for Enrollment, containing common attributes
    # Foreign keys to link to Student and Course tables
    student_id: int = Field(foreign_key="student.id")
    course_id: int = Field(foreign_key="course.id")

class Enrollment(EnrollmentBase, table=True):
    # Enrollment model for database table, inherits from EnrollmentBase
    id: Optional[int] = Field(default=None, primary_key=True)

# API Routes

@app.post("/students/", response_model=Student)
def create_student(student: StudentBase, session: Session = Depends(get_session)):
    # Create a new student in the database
    db_student = Student.model_validate(student)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[Student])
def read_students(session: Session = Depends(get_session)):
    # Retrieve all students from the database
    students = session.exec(select(Student)).all()
    return students

@app.post("/courses/", response_model=Course)
def create_course(course: CourseBase, session: Session = Depends(get_session)):
    # Create a new course in the database
    db_course = Course.model_validate(course)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

@app.get("/courses/", response_model=List[Course])
def read_courses(session: Session = Depends(get_session)):
    # Retrieve all courses from the database
    courses = session.exec(select(Course)).all()
    return courses

@app.post("/enrollments/", response_model=Enrollment)
def create_enrollment(enrollment: EnrollmentBase, session: Session = Depends(get_session)):
    # Create a new enrollment in the database
    db_enrollment = Enrollment.model_validate(enrollment)
    session.add(db_enrollment)
    session.commit()
    session.refresh(db_enrollment)
    return db_enrollment

@app.get("/enrollments/", response_model=List[Enrollment])
def read_enrollments(session: Session = Depends(get_session)):
    # Retrieve all enrollments from the database
    enrollments = session.exec(select(Enrollment)).all()
    return enrollments

@app.get("/")
def read_root():
    # Root endpoint, returns a welcome message
    return {"message": "Welcome to The Xavier Institute API"}

# Initialize the database
# This creates all the tables in the database