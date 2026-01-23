from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
import calendar

from app.database.session import get_db
from app.models import Class, Student
from app.services import teacher_service
from app.utils.helpers import initials
from app.core.config import Settings
from app.core.dependencies import get_current_user

# Initialize templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/teacher", tags=["teacher"])


@router.get("-dashboard", name="teacher_dashboard")
def show_teacher_dashboard(request: Request, user: str = Depends(get_current_user)):

    return templates.TemplateResponse("teacher_dashboard.html", {"request": request})


@router.get("/classes", name="teacher_classes")
def show_teacher_classes(request: Request, user: str = Depends(get_current_user)):

    return templates.TemplateResponse("teacher_classes.html", {"request": request})


@router.get("/classes/details", name="teacher_class_details")
def show_teacher_class_details(
    request: Request,
    class_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):

    # Fetch class info
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        print("Class is not found")
        raise HTTPException(status_code=404, detail="Class not found")

    # name,init,roll_no
    student_data = []

    # result
    result = (
        db.query(Student.id, Student.name)
        .filter(Student.class_id == class_id)
        .order_by(Student.name.asc())
        .all()
    )

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


@router.get("/students/data", name="get_student_data")
def get_student_data(
    request: Request,
    month: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):

    try:
        # Convert month name to number (e.g., "January" -> 1)
        month_obj = datetime.strptime(month, "%B")
        month_num = month_obj.month
    except ValueError:
        return []

    class_id = 11
    year = datetime.now().year  # Using current context year

    students_data = teacher_service.get_students_for_classes(
        db, class_id, month_num, year
    )

    return students_data


@router.get("/students", name="teacher_students")
def show_teacher_students(
    request: Request,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    class_id = 11

    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_month_name = now.strftime("%B")

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


@router.get("/api/classes-list", name="get_all_classes_data")
def get_all_classes_data(
    request: Request,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):

    from sqlalchemy import func
    from app.models import Student

    # Load teacher's specific classes from demo.json
    try:
        teacher_classes = Settings.JSON_DATA.get("teacher_classes", [])
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
