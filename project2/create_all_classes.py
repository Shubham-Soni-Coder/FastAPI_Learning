"""
Database Seeding Script
=======================

This script is used to populate the database with initial data.
It includes functions to create classes, students, and fee structures from a JSON source.
"""

from app.database import engine, Base, session
from app.models import (
    Base,
    User,
    Class,
    Subject,
    ClassSubject,
    Student,
    StudentSubject,
    FeesStructure,
    FeesComponent,
    StudentFeesDue,
    FeesPayment,
    AttendanceSession,
    AttendanceRecord,
)
from app.schemas import (
    ClassCreate,
    ClassSubjectCreate,
    SubjectCreate,
    StudentCreate,
    FeesStructureCreate,
    FeesComponentCreate,
    StudentFeesDueCreate,
    FeesPaymentCreate,
    AttendanceSessionCreate,
    AttendanceRecordCreate,
)
import json
from datetime import datetime, date
import random
import calendar
from itertools import chain
from app.function import normalize, load_data, conn_database

# load the data from json file
JSON_DATA = load_data()


# store in database
Base.metadata.create_all(bind=engine)

db = session()


# make a constent class
def create_class():
    starting = ["1st", "2nd", "3rd"]
    after = [f"{i}th" for i in range(4, 13)]
    streams = ["non-medical", "medical", "arts", "commerce"]

    classes = starting + after

    for cl in classes:
        int_cl = int(cl[:-2])  # remove last two
        if int_cl <= 10:
            schema = ClassCreate(class_name=cl, stream=None)
            model = Class(**schema.model_dump())
            db.add(model)
        else:
            for stream in streams:
                schema = ClassCreate(class_name=cl, stream=stream)
                model = Class(**schema.model_dump())
                db.add(model)
    db.commit()


def create_student():

    data = JSON_DATA

    classes = db.query(Class).all()

    for i, user in enumerate(data["students"]):
        class_obj = classes[i % len(classes)]  # roation with %
        schems = StudentCreate(
            name=user["name"],
            father_name=user["father_name"],
            mother_name=user["mother_name"],
            email=user["email"],
            hashed_password=user["hashed_password"],
            is_active=user["is_active"],
            class_id=class_obj.id,
        )
        model = Student(**schems.model_dump())
        db.add(model)
    db.commit()


def create_fees_structure():
    classes = db.query(Class).all()
    number = len(classes)
    academic_year = "2025-26"
    for cls in classes:
        schems = FeesStructureCreate(
            class_id=cls.id, academic_year=academic_year, is_active=True
        )
        model = FeesStructure(**schems.model_dump())
        db.add(model)
    db.commit()


def create_fees_component():
    data = JSON_DATA["fees_by_class"]

    class_data = list(data.keys())
    fees_data = db.query(FeesStructure).all()

    for i, key in zip(class_data, fees_data):
        for fees in data[i]:
            schems = FeesComponentCreate(
                fees_structure_id=key.id,
                component_name=fees["component_name"],
                amount=fees["amount"],
            )
            model = FeesComponent(**schems.model_dump())
            db.add(model)
    db.commit()


def create_student_fees_due():
    class_id = 11
    ids = [
        i[0] for i in db.query(Student.id).filter(Student.class_id == class_id).all()
    ]
    for id in ids:
        schems = StudentFeesDueCreate(
            student_id=id,
            month=1,
            year=2025,
            total_amount=4000,
            status="pending",
        )
        model = StudentFeesDue(**schems.model_dump())
        db.add(model)
    db.commit()


def create_fees_payment():

    Student_ids = [21, 22, 23, 24, 25]

    due_id = [
        i[0]
        for i in db.query(StudentFeesDue.id)
        .filter(StudentFeesDue.student_id.in_(Student_ids))
        .all()
    ]

    for id in due_id:
        schems = FeesPaymentCreate(
            due_id=id,
            amount_paid=4000,
            discount_amount=0,
            fine_amount=0,
            method="online",
            is_late=False,
        )
        model = FeesPayment(**schems.model_dump())
        db.add(model)
    db.commit()


def create_attendance_session():

    sessions = []
    class_id = 11
    session_name = "Morning"
    year = 2025

    for month in range(4, 13):  # april to december
        days_in_month = calendar.monthrange(2025, month)[1]

        for day in range(1, days_in_month + 1):
            schems = AttendanceSessionCreate(
                class_id=class_id,
                date=date(year, month, day),  # proper date object
                session_name=session_name,
            )
            model = AttendanceSession(**schems.model_dump())
            sessions.append(model)

    db.add_all(sessions)
    db.commit()


def create_attendance_record():
    class_id = 11
    session_ids = [
        i[0]
        for i in db.query(AttendanceSession.id)
        .filter(AttendanceSession.class_id == class_id)
        .all()
    ]
    student_ids = [
        i[0] for i in db.query(Student.id).filter(Student.class_id == class_id).all()
    ]

    records = []

    for session_id in session_ids:
        for student_id in student_ids:
            schems = AttendanceRecordCreate(
                session_id=session_id,
                student_id=student_id,
                status=random.choice(["present", "absent"]),
            )
            model = AttendanceRecord(**schems.model_dump())
            records.append(model)
    db.add_all(records)
    db.commit()


def update_status():
    """In this function we update the data acc. to the payment data
    if amount_paid == total_amount then status = 'paid'"""

    due_id = db.query(StudentFeesDue).all()
    for due in due_id:
        payment = db.query(FeesPayment).filter(FeesPayment.due_id == due.id).first()
        if payment.amount_paid == due.total_amount:
            due.status = "paid"
            db.add(due)
    db.commit()


def add_data():
    # add data in database
    # for i in range(1, 31):
    #     date = datetime(2025, 11, i)
    #     schems = AttendanceSessionCreate(class_id=11, date=date, session_name="Morning")
    #     model = AttendanceSession(**schems.model_dump())
    #     db.add(model)
    # db.commit()
    session_id = [
        i[0]
        for i in db.query(AttendanceSession.id)
        .filter(AttendanceSession.class_id == 11)
        .filter(AttendanceSession.id != 1)
        .all()
    ]

    student_id = [
        i[0] for i in db.query(Student.id).filter(Student.class_id == 11).all()
    ]

    for i in student_id:
        for j in session_id:
            schems = AttendanceRecordCreate(
                session_id=j,
                student_id=i,
                status=random.choice(("absent", "present")),
            )
            model = AttendanceRecord(**schems.model_dump())
            db.add(model)
    db.commit()


def show_data():
    # feesdata = db.query(FeesPayment).all()
    # for data in feesdata:
    #     print(
    #         data.due_id,
    #         data.amount_paid,
    #         data.discount_amount,
    #         data.fine_amount,
    #         data.method,
    #         data.is_late,
    #     )
    datas = db.query(StudentFeesDue).all()
    for data in datas:
        print(
            data.id,
            data.student_id,
            data.month,
            data.year,
            data.total_amount,
            data.status,
        )


def create_subject():
    Subject_data = JSON_DATA["Subjects"]

    def add_subject(nane):
        schems = SubjectCreate(name=nane)
        model = Subject(**schems.model_dump())
        db.add(model)

    unique_subjects = set()

    # common
    for s in Subject_data.get("Common", []):
        unique_subjects.add(s)

    # optional
    for s in Subject_data.get("Optional", []):
        unique_subjects.add(s)

    # Stream
    for stream_subject in Subject_data.get("Streams", {}).values():
        for s in stream_subject:
            unique_subjects.add(s)

    # Add at once
    for name in unique_subjects:
        add_subject(name)
    db.commit()


def insert(class_id, subject_name, category, stream, compulsory, main):

    # get data using name
    subject_data = {s.name: s.id for s in db.query(Subject).all()}
    subject_id = subject_data.get(subject_name)

    if not subject_id:
        None

    exists = (
        db.query(ClassSubject)
        .filter_by(class_id=class_id, subject_id=subject_id)
        .first()
    )

    if exists:
        None

    schems = ClassSubjectCreate(
        class_id=class_id,
        subject_id=subject_id,
        category=category,
        stream=stream,
        is_compulsory=compulsory,
        is_main=main,
    )

    model = ClassSubject(**schems.model_dump())
    db.add(model)


def create_class_subject():
    subjects_json = JSON_DATA["Subjects"]

    classes = db.query(Class).all()

    for cls in classes:
        cno = cls.id
        cstr = cls.stream

        # common (1-12)
        for s in subjects_json.get("Common", []):
            insert(cls.id, normalize(s), "common", None, True, True)
        # optional (6-12)
        if cno >= 6:
            for s in subjects_json.get("Optional", []):
                insert(cls.id, normalize(s), "optional", None, False, False)

        # for science srteam
        if cstr == "science":
            for s in subjects_json.get("Science", {}).get("Medical", []):
                insert(cls.id, normalize(s), "stream", "science", True, True)

            for s in subjects_json.get("Science", {}).get("Non-Medical", []):
                insert(cls.id, normalize(s), "stream", "science", True, True)

            for s in subjects_json.get("Science", {}).get("Optional", []):
                insert(cls.id, normalize(s), "optional", "science", False, False)

        # for commerce srteam
        elif cstr == "commerce":
            for s in subjects_json.get("Commerce", {}).get("Core", []):
                insert(cls.id, normalize(s), "stream", "commerce", True, True)

            for s in subjects_json.get("Commerce", {}).get("Optional", []):
                insert(cls.id, normalize(s), "optional", "commerce", False, False)

        # for humanities srteam
        elif cstr == "humanities":
            for s in subjects_json.get("Humanities", {}).get("Core", []):
                insert(cls.id, normalize(s), "stream", "humanities", True, True)

            for s in subjects_json.get("Humanities", {}).get("Optional", []):
                insert(cls.id, normalize(s), "optional", "humanities", False, False)

    db.commit()


def drop_table():
    # remove data from attendance_records where session_id is 276
    db.query(AttendanceRecord).filter(AttendanceRecord.session_id == 276).delete()
    db.commit()


if __name__ == "__main__":
    # create_fees_component()
    # create_student()
    # create_fees_structure()
    # create_student_fees_due()
    # update_status()
    # show_data()
    drop_table()
    # create_fees_payment()
    # create_attendance_session()
    # create_attendance_record()
    # add_data()
    # create_subject()
    # create_class_subject()
