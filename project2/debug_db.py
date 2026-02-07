from app.database.session import SessionLocal
from app.models import Teacher, ClassSchedule, Subject

db = SessionLocal()

print("--- Teachers ---")
teachers = db.query(Teacher).all()
for t in teachers:
    print(f"ID: {t.id}, Name: {t.full_name}, UserID: {t.user_id}")

print("\n--- Subjects ---")
subjects = db.query(Subject).all()
for s in subjects:
    print(f"ID: {s.id}, Name: {s.name}")

print("\n--- Class Schedules ---")
schedules = db.query(ClassSchedule).all()
for s in schedules:
    print(
        f"ID: {s.id}, TeacherID: {s.teacher_id}, Day: {s.day_of_week}, Start: {s.start_time}, SubjectID: {s.subject_id}"
    )

db.close()
