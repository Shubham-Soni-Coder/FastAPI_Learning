"""
Main Application Module
=======================

This module initializes the FastAPI application and defines the route handlers.
It includes routes for authentication (login, register), dashboard views, and teacher functionalities.
"""

from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Depends
from sqlalchemy.orm import Session
import hashlib
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime, timedelta
import calendar
from app.schemas import UserCreate, Usermodel
import os
import json
from dotenv import load_dotenv
from app.database import get_db, Base, engine
from app.models import User, OTP, Student, StudentFeesDue, Class
from app.otp_sender import send_otp, verify_otp
from app.database import session
from app.function import count_student_present_day, initilas, conn_database, load_data

# load the data
load_dotenv()
JSON_data = load_data()
# load the sercet key
secret_key = os.getenv("SECRET_KEY")

# Safety check: Stop the app if the key is missing
if secret_key is None:
    raise ValueError("No SECRET_KEY found in .env file!")

app = FastAPI()

# make database
db = session()

# Static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


# Templates
templates = Jinja2Templates(directory="templates")

# hashed password add
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# add security
app.add_middleware(
    SessionMiddleware,
    secret_key=secret_key,
    same_site="lax",
    https_only=False,  # True in production
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return RedirectResponse(url="/static/images/favicon.ico")


@app.get("/", name="login_page")
def show_form(request: Request):
    # Security check: exist session
    if "gmail" in request.session:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login_page.html", {"request": request})


@app.get("/register", name="register")
def show_register_form(request: Request):
    return templates.TemplateResponse("register_page.html", {"request": request})


@app.get("/dashboard", name="dashboard")
def show_dashboard(request: Request):
    # Security check: exist session
    if "gmail" not in request.session:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/teacher-dashboard", name="teacher_dashboard")
def show_teacher_dashboard(request: Request):
    # Security check: exist session
    if "gmail" not in request.session:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("teacher_dashboard.html", {"request": request})


@app.get("/teacher/classes", name="teacher_classes")
def show_teacher_classes(request: Request):
    # Security check: exist session
    if "gmail" not in request.session:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("teacher_classes.html", {"request": request})


@app.get("/teacher/classes/details", name="teacher_class_details")
def show_teacher_class_details(
    request: Request,
    class_id: int = 11,
    db: Session = Depends(get_db),
):
    # Security check: exist session
    if "gmail" not in request.session:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    # Fetch class info
    class_info = db.query(Class).filter(Class.id == class_id).first()

    # name,init,roll_no
    student_data = []

    # result
    query = "SELECT name FROM students WHERE class_id = ? ORDER BY name ASC"
    result = conn_database(query, (class_id,))
    for i, row in enumerate(result):
        student_data.append(
            {
                "roll_no": i + 1,
                "name": row[0],
                "initials": initilas(row[0]),
            }
        )

    return templates.TemplateResponse(
        "teacher_class_details.html",
        {"request": request, "students": student_data, "class_info": class_info},
    )


@app.get("/teacher/students/data", name="get_student_data")
def get_student_data(request: Request, month: str, db: Session = Depends(get_db)):
    if "gmail" not in request.session:
        return {"error": "Unauthorized"}

    try:
        # Convert month name to number (e.g., "January" -> 1)
        month_obj = datetime.strptime(month, "%B")
        month_num = month_obj.month
    except ValueError:
        return []

    class_id = 11
    year = 2025  # Using current context year

    # Get total days in the selected month
    _, total_days_in_month = calendar.monthrange(year, month_num)

    # Query Students
    results = (
        db.query(Student, StudentFeesDue)
        .join(Class, Student.class_id == Class.id)
        .join(StudentFeesDue, Student.id == StudentFeesDue.student_id)
        .filter(Class.id == class_id)
        .order_by(Student.name.asc())
        .all()
    )

    students_data = []

    for i, (student, fees) in enumerate(results):
        days_present = count_student_present_day(db, student.id, year, month_num)

        # Calculate attendance percentage
        attendance_percentage = (
            round((days_present / total_days_in_month) * 100)
            if total_days_in_month > 0
            else 0
        )

        parts = student.name.strip().split()
        initials = (
            parts[0][0] if len(parts) == 1 else parts[0][0] + parts[-1][0]
        ).upper()

        students_data.append(
            {
                "roll_no": i + 1,
                "name": student.name,
                "father_name": student.father_name,
                "fees_paid": fees.status,
                "attendance": attendance_percentage,
                "days_present": days_present,
                "total_days": total_days_in_month,
                "initials": initials,
            }
        )

    return students_data


@app.get("/teacher/students", name="teacher_students")
def show_teacher_students(request: Request):
    if "gmail" not in request.session:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    class_id = 11

    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_month_name = now.strftime("%B")

    # Get total days in the current month
    _, total_days_in_month = calendar.monthrange(current_year, current_month)

    # Mock Data for student list
    results = (
        db.query(Student, StudentFeesDue)
        .join(Class, Student.class_id == Class.id)
        .join(StudentFeesDue, Student.id == StudentFeesDue.student_id)
        .filter(Class.id == class_id)
        .order_by(Student.name.asc())
        .all()
    )

    students_data = []

    for i, (student, fees) in enumerate(results):
        days_present = count_student_present_day(
            db, student.id, current_year, current_month
        )

        # Calculate attendance percentage
        attendance_percentage = (
            round((days_present / total_days_in_month) * 100)
            if total_days_in_month > 0
            else 0
        )

        # Initalital calculate
        initials = initilas(student.name)

        # add data in list
        students_data.append(
            {
                "roll_no": i + 1,
                "name": student.name,
                "father_name": student.father_name,
                "fees_paid": fees.status,
                "attendance": attendance_percentage,
                "days_present": days_present,
                "total_days": total_days_in_month,
                "initials": initials,
            }
        )

    return templates.TemplateResponse(
        "teacher_students.html",
        {
            "request": request,
            "students": students_data,
            "current_month_name": current_month_name,
        },
    )


@app.post("/register", name="register")
def register_user(
    request: Request,
    usergmail: str = Form(...),
    userpassword: str = Form(...),
    db: Session = Depends(get_db),
):

    # hash the password
    # pwd_context is now global

    hashed_password = pwd_context.hash(userpassword)

    # check existing gmail
    existing = db.query(User).filter(User.gmail_id == usergmail).first()

    if existing:
        # delete data just for testing
        print("data is already exist")
        hashed_password = None
        return templates.TemplateResponse(
            "register_page.html", {"request": request, "error": "Email already in use"}
        )

    send_otp(usergmail)
    request.session["gmail"] = usergmail
    request.session["password"] = hashed_password
    request.session["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return templates.TemplateResponse(
        "otp_send_page.html", {"request": request, "usergmail": usergmail}
    )


@app.post("/login_success", name="login_success")
def show_login_success(
    request: Request,
):
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/otp_send", name="otp_send")
def otp_sender(request: Request, usergmail: str = Form(...), password: str = Form(...)):

    send_otp(usergmail)

    request.session["gmail"] = usergmail  # This is a cookie for brower

    return templates.TemplateResponse("otp_send_page.html", {"request": request})


@app.post("/verify-otp", name="verify_otp")
def verify_otp_code(
    request: Request,
    otp: str = Form(...),
    db: Session = Depends(get_db),
):

    gmail = request.session.get("gmail")
    password = request.session.get("password")
    timestamp = request.session.get("time")

    if not gmail:
        print("Session expried error")
        return templates.TemplateResponse(
            "otp_send_page.html",
            {"request": request, "error": "Session expired. Try again."},
        )

    is_valid = verify_otp(gmail, otp)

    if not is_valid:
        print("Otp not match")
        return templates.TemplateResponse(
            "otp_send_page.html",
            {"request": request, "error": "Invalid or expired OTP"},
        )

    user = User(gmail_id=gmail, password=password)
    db.add(user)
    db.commit()
    print("Data sucessful added")
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/login", name="login")
def login(
    request: Request,
    usergmail: str = Form(...),
    userpassword: str = Form(...),
    db: Session = Depends(get_db),
):
    # check for existing user
    user = db.query(User).filter(User.gmail_id == usergmail).first()

    if not user:
        print("User not found")
        return templates.TemplateResponse(
            "login_page.html",
            {"request": request, "error": "Email address is not found"},
        )

    # verify password
    if not pwd_context.verify(userpassword, user.password):
        print("Password is incorrect")
        return templates.TemplateResponse(
            "login_page.html",
            {"request": request, "error": "Invalid password"},
        )

    # Store user in session
    request.session["gmail"] = usergmail

    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/teacher/api/classes-list", name="get_all_classes_data")
def get_all_classes_data(request: Request, db: Session = Depends(get_db)):
    if "gmail" not in request.session:
        return {"error": "Unauthorized"}

    from sqlalchemy import func

    # Load teacher's specific classes from demo.json
    try:
        teacher_classes = JSON_data.get("teacher_classes", [])
    except Exception as e:
        print(f"Error reading demo.json: {e}")
        return []

    results = []

    for cls_data in teacher_classes:
        class_id = cls_data["id"]

        # Count students in this class from Real Database
        student_count = (
            db.query(func.count(Student.id))
            .filter(Student.class_id == class_id)
            .scalar()
        )

        # Combine static demo data with dynamic DB count
        results.append(
            {
                "id": class_id,
                "name": cls_data["name"],
                "subject": cls_data["subject"],
                "students": student_count,
                "time": cls_data["time"],
            }
        )

    return results
