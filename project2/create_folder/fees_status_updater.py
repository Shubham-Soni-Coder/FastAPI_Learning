from sqlalchemy import func
from app.database.session import SessionLocal
from app.models import StudentFeesDue, FeesPayment


def update_fees_due_status():
    db = SessionLocal()
    try:
        # Get all fee due records
        due_records = db.query(StudentFeesDue).all()

        updated_count = 0

        for due in due_records:
            # Calculate total paid for this specific due record
            total_paid = (
                db.query(func.sum(FeesPayment.amount_paid))
                .filter(FeesPayment.due_id == due.id)
                .scalar()
                or 0.0
            )

            # Determine correct status
            new_status = "paid" if total_paid >= due.total_amount else "pending"

            # Only update if status has changed
            if due.status != new_status:
                due.status = new_status
                updated_count += 1

        db.commit()
        print(f"Successfully updated {updated_count} fee status records.")

    except Exception as e:
        db.rollback()
        print(f"Error updating fee status: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    update_fees_due_status()
