from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import calendar

from app.database.session import get_db
from app.models import Batches, Student, Teacher, ClassSchedule
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

    # Fetch upcoming classes
    now = datetime.now()
    day = now.weekday() + 1
    current_time = now.time()

    upcoming_classes = teacher_service.get_upcoming_classes(
        db, teacher.id, day, current_time
    )

    upcoming_classes_data = []
    for cls in upcoming_classes:
        student_count = (
            db.query(func.count(Student.id))
            .filter(Student.batch_id == cls.batch_id)
            .scalar()
        )

        upcoming_classes_data.append(
            {
                "batch_id": cls.batch_id,
                "batch_name": cls.batch.batch_name if cls.batch else "Class",
                "subject": cls.subject.name if cls.subject else "N/A",
                "time": cls.start_time.strftime("%I:%M %p"),
                "student_count": student_count,
            }
        )

    # Fetch dynamic stats
    total_classes = (
        db.query(func.count(ClassSchedule.id))
        .filter(ClassSchedule.teacher_id == teacher.id)
        .scalar()
    )

    # Get all batch IDs for this teacher
    teacher_batch_ids = (
        db.query(ClassSchedule.batch_id)
        .filter(ClassSchedule.teacher_id == teacher.id)
        .distinct()
        .all()
    )
    teacher_batch_ids = [r[0] for r in teacher_batch_ids]

    total_students = (
        db.query(func.count(Student.id))
        .filter(Student.batch_id.in_(teacher_batch_ids))
        .scalar()
        if teacher_batch_ids
        else 0
    )

    return templates.TemplateResponse(
        "teacher_dashboard.html",
        {
            "request": request,
            "teacher": teacher_data,
            "upcoming_classes": upcoming_classes_data,
            "stats": {
                "total_students": total_students,
                "active_classes": total_classes,
                "pending_review": 12,  # Still hardcoded as per plan
                "rating": 4.8,  # Still hardcoded as per plan
            },
        },
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

    # Verify teacher teaches this batch
    is_authorized = (
        db.query(ClassSchedule)
        .filter(
            ClassSchedule.teacher_id == teacher.id, ClassSchedule.batch_id == batch_id
        )
        .first()
    )
    if not is_authorized:
        raise HTTPException(status_code=403, detail="Not authorized to view this batch")

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
    batch_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_teacher),
):
    teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
    if not teacher:
        return []

    # Verify teacher teaches this batch
    is_authorized = (
        db.query(ClassSchedule)
        .filter(
            ClassSchedule.teacher_id == teacher.id, ClassSchedule.batch_id == batch_id
        )
        .first()
    )
    if not is_authorized:
        return []

    try:
        # Convert month name to number (e.g., "January" -> 1)
        month_obj = datetime.strptime(month, "%B")
        month_num = month_obj.month
    except ValueError:
        return []

    year = 2025

    students_data = teacher_service.get_students_for_batch(
        db, batch_id, month_num, year
    )

    return students_data


@router.get("/students", name="teacher_students")
def show_teacher_students(
    request: Request,
    batch_id: int = None,
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

    # Fetch all batches for this teacher to populate a dropdown
    schedules = (
        db.query(ClassSchedule).filter(ClassSchedule.teacher_id == teacher.id).all()
    )

    # Unique batches
    teacher_batches = {}
    for s in schedules:
        if s.batch_id not in teacher_batches:
            teacher_batches[s.batch_id] = s.batch.batch_name

    batches_list = [
        {"id": bid, "name": bname} for bid, bname in teacher_batches.items()
    ]

    # If no batch_id specified, pick the first one from teacher's batches
    if not batch_id and batches_list:
        batch_id = batches_list[0]["id"]

    current_batch_name = "No Batch Selected"
    students_data = []

    if batch_id:
        # Verify teacher teaches this batch
        if batch_id not in teacher_batches:
            raise HTTPException(
                status_code=403, detail="Not authorized to view this batch"
            )

        current_batch_name = teacher_batches[batch_id]

        # Get current date
        now = datetime.now()
        current_year = 2025
        current_month = now.month

        students_data = teacher_service.get_students_for_batch(
            db, batch_id, current_month, current_year
        )

    current_month_name = datetime.now().strftime("%B")

    return templates.TemplateResponse(
        "teacher_students.html",
        {
            "request": request,
            "students": students_data,
            "current_month_name": current_month_name,
            "teacher": teacher_data,
            "batches": batches_list,
            "current_batch_id": batch_id,
            "current_batch_name": current_batch_name,
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
    # Query classes for this teacher
    classes = (
        db.query(ClassSchedule).filter(ClassSchedule.teacher_id == teacher.id).all()
    )

    results = []
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    for cls in classes:
        # Count students in this batch (real DB count)
        student_count = (
            db.query(func.count(Student.id))
            .filter(Student.batch_id == cls.batch_id)
            .scalar()
        )

        day_name = days[cls.day_of_week - 1] if 1 <= cls.day_of_week <= 7 else "Unknown"

        results.append(
            {
                "id": cls.batch_id,
                "name": cls.name,
                "subject": cls.subject.name,
                "students": student_count,
                "time": (
                    f"{day_name} {cls.start_time.strftime('%I:%M %p')}"
                    if cls.start_time
                    else "N/A"
                ),
                "day_code": cls.day_of_week,
            }
        )

    return results
