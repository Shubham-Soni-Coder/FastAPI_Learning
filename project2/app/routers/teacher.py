from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import calendar

from app.database.session import get_db
from app.models import Batches, Student, Teacher, Class
from app.services import teacher_service
from app.utils.helpers import initials
from app.core.config import Settings
from app.core.dependencies import get_current_teacher

# Initialize templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/teacher", tags=["teacher"])


@router.get("/dashboard", name="teacher_dashboard")
def show_teacher_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_teacher),
):
    teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    teacher_data = {
        "full_name": teacher.full_name,
        "department": teacher.department,
        "initials": initials(teacher.full_name),
    }

    return templates.TemplateResponse(
        "teacher_dashboard.html", {"request": request, "teacher": teacher_data}
    )


@router.get("/classes", name="teacher_classes")
def show_teacher_classes(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_teacher),
):
    teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    teacher_data = {
        "full_name": teacher.full_name,
        "department": teacher.department,
        "initials": initials(teacher.full_name),
    }

    return templates.TemplateResponse(
        "teacher_classes.html", {"request": request, "teacher": teacher_data}
    )


@router.get("/classes/details", name="teacher_class_details")
def show_teacher_class_details(
    request: Request,
    batch_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_teacher),
):
    teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    teacher_data = {
        "full_name": teacher.full_name,
        "department": teacher.department,
        "initials": initials(teacher.full_name),
    }

    # Fetch class info
    class_obj = db.query(Batches).filter(Batches.id == batch_id).first()
    if not class_obj:
        print("Batch is not found")
        raise HTTPException(status_code=404, detail="Batch not found")

    # name,init,roll_no
    student_data = []

    # result
    result = (
        db.query(Student.id, Student.name)
        .filter(Student.batch_id == batch_id)
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
            "batch_id": class_obj.id,
            "batch_name": class_obj.batch_name,
            "mode": "start",
            "teacher": teacher_data,
        },
    )


@router.get("/students/data", name="get_student_data")
def get_student_data(
    request: Request,
    month: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_teacher),
):

    try:
        # Convert month name to number (e.g., "January" -> 1)
        month_obj = datetime.strptime(month, "%B")
        month_num = month_obj.month
    except ValueError:
        return []

    batch_id = 11
    year = 2025  # Using current context year

    students_data = teacher_service.get_students_for_batch(
        db, batch_id, month_num, year
    )

    return students_data


@router.get("/students", name="teacher_students")
def show_teacher_students(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_teacher),
):
    teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    teacher_data = {
        "full_name": teacher.full_name,
        "department": teacher.department,
        "initials": initials(teacher.full_name),
    }
    batch_id = 11

    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_month_name = now.strftime("%B")

    # Get total days in the current month
    students_data = teacher_service.get_students_for_batch(
        db, batch_id, current_month, current_year
    )

    return templates.TemplateResponse(
        "teacher_students.html",
        {
            "request": request,
            "students": students_data,
            "current_month_name": current_month_name,
            "teacher": teacher_data,
        },
    )


@router.get("/api/classes-list", name="get_all_classes_data")
def get_all_classes_data(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_teacher),
):
    # Fetch teacher profile
    teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
    if not teacher:
        return []

    # Query classes for this teacher
    classes = db.query(Class).filter(Class.teacher_id == teacher.id).all()

    results = []

    for cls in classes:
        # Count students in this batch (real DB count)
        student_count = (
            db.query(func.count(Student.id))
            .filter(Student.batch_id == cls.batch_id)
            .scalar()
        )

        results.append(
            {
                "id": cls.batch_id,
                "name": cls.name,
                "subject": cls.subject,
                "students": student_count,
                "time": (
                    cls.start_time.strftime("%I:%M %p") if cls.start_time else "N/A"
                ),
            }
        )

    return results
