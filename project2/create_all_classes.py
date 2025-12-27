"""
Database Seeding Script
=======================

This script is used to populate the database with initial data.
It includes functions to create classes, students, and fee structures from a JSON source.
"""

from app.database import engine, Base, get_db, session
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
)
from app.schemas import (
    ClassCreate,
    SubjectCreate,
    StudentCreate,
    FeesStructureCreate,
    FeesComponentCreate,
    StudentFeesDueCreate,
    FeesPaymentCreate,
)
import json

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

    with open("demo.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    classes = db.query(Class).all()

    for i, (gmail, user) in enumerate(data["students"].items()):
        class_obj = classes[i % len(classes)]  # roation with %
        schems = StudentCreate(
            roll_no=user["roll_no"],
            name=user["name"],
            father_name=user["father_name"],
            mother_name=user["mother_name"],
            email=gmail,
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
    with open("demo.json", "r") as f:
        data = json.load(f)
        data = data["fees_by_class"]

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
    students = db.query(Student).all()
    for student in students:
        schems = StudentFeesDueCreate(
            student_id=student.id,
            month=1,
            year=2025,
            total_amount=4000,
            status="pending",
        )
        model = StudentFeesDue(**schems.model_dump())
        db.add(model)
    db.commit()


def create_fees_payment():
    due_id = db.query(StudentFeesDue).all()
    for due in due_id:
        schems = FeesPaymentCreate(
            due_id=due.id,
            amount_paid=4000,
            discount_amount=0,
            fine_amount=0,
            method="online",
            is_late=False,
        )
        model = FeesPayment(**schems.model_dump())
        db.add(model)
    db.commit()


def show_data():
    feesdata = db.query(FeesPayment).all()
    for data in feesdata:
        print(
            data.due_id,
            data.amount_paid,
            data.discount_amount,
            data.fine_amount,
            data.method,
            data.is_late,
        )
    # datas = db.query(StudentFeesDue).all()
    # for data in datas:
    #     print(
    #         data.id,
    #         data.student_id,
    #         data.month,
    #         data.year,
    #         data.total_amount,
    #         data.status,
    #     )


def drop_table():
    from sqlalchemy import text

    db.execute(text("DROP TABLE IF EXISTS fee_payments"))
    db.commit()


if __name__ == "__main__":
    # create_fees_structure()
    # create_student_fees_due()
    show_data()
    # drop_table()
    # create_fees_payment()
