"""
Main Application Module
=======================

This module initializes the FastAPI application and defines the route handlers.
It includes routes for authentication (login, register), dashboard views, and teacher functionalities.
"""

from fastapi import FastAPI, Request, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Depends
from sqlalchemy.orm import Session
import hashlib
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime, timedelta
import calendar

from app.models import Class, Student
from app.services.otp_service import send_otp
from app.services import auth_service, teacher_service
from app.utils.helpers import initials
from app.function import conn_database
from app.routers import attendance
from app.core.middleware import setup_middleware
from app.database.session import SessionLocal, engine, get_db
from app.database.base import Base
from app.core.config import Settings
from app.core.exceptions import CustomException

# load the data
JSON_DATA = Settings.JSON_DATA

app = FastAPI()

# make database
db = SessionLocal()

# Include Routers
app.include_router(attendance.router)

# Static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


# Templates
templates = Jinja2Templates(directory="templates")


# add security
setup_middleware(app)


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
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        print("Class is not found")
        raise HTTPException(status_code=404, detail="Class not found")

    # name,init,roll_no
    student_data = []

    # result
    query = "SELECT id , name FROM students where class_id = ? ORDER BY name ASC"
    result = conn_database(query, (class_id,))
    for i, row in enumerate(result):
        student_data.append(
            {
                "roll_no": i + 1,
                "student_id": row[0],
                "name": row[1],
                "initials": initials(row[1]),
            }
        )

    return templates.TemplateResponse(
        "teacher_class_details.html",
        {
            "request": request,
            "students": student_data,
            "class_id": class_obj.id,
            "class_name": class_obj.class_name,
            "mode": "start",
        },
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
    class_id = 11
    year = 2025  # Using current context year

    students_data = teacher_service.get_students_for_classes(
        db, class_id, month_num, year
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
    # Get total days in the current month
    students_data = teacher_service.get_students_for_classes(
        db, class_id, current_month, current_year
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

    try:
        auth_service.start_register(db, usergmail, userpassword, request.session)
    except CustomException as e:
        return templates.TemplateResponse(
            "register_page.html", {"request": request, "error": e.detail}
        )

    return templates.TemplateResponse(
        "otp_send_page.html", {"request": request, "usergmail": usergmail}
    )


@app.post("/login_success", name="login_success")
def show_login_success(
    request: Request,
):
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/otp_send", name="otp_send")
def otp_sender(
    request: Request,
    usergmail: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    send_otp(usergmail, db)

    request.session["gmail"] = usergmail  # This is a cookie for brower

    return templates.TemplateResponse("otp_send_page.html", {"request": request})


@app.post("/verify-otp", name="verify_otp")
def verify_otp_code(
    request: Request,
    otp: str = Form(...),
    db: Session = Depends(get_db),
):

    try:
        auth_service.complet_register(db, request.session, otp)
        print("Data sucessful added")
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    except CustomException as e:
        return templates.TemplateResponse(
            "otp_send_page.html",
            {"request": request, "error": e.detail},
        )


@app.post("/login", name="login")
def login(
    request: Request,
    usergmail: str = Form(...),
    userpassword: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        auth_service.login_user(db, usergmail, userpassword, request.session)
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    except CustomException as e:
        return templates.TemplateResponse(
            "login_page.html",
            {"request": request, "error": e.detail},
        )

    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/teacher/api/classes-list", name="get_all_classes_data")
def get_all_classes_data(request: Request, db: Session = Depends(get_db)):
    if "gmail" not in request.session:
        return {"error": "Unauthorized"}

    from sqlalchemy import func

    # Load teacher's specific classes from demo.json

    try:
        teacher_classes = JSON_DATA.get("teacher_classes", [])
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
