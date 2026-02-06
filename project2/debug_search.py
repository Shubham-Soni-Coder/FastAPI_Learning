from app.database.session import SessionLocal
from app.services.teacher_service import get_students_for_batch
import json

db = SessionLocal()
try:
    # Testing search for "An" in Batch 10 (or whatever batches exist)
    # Let's check what batches belong to a teacher first if possible
    data = get_students_for_batch(db, batch_id=10, month=3, year=2025, search="An")
    print("Search Results for 'An' in Batch 10:")
    print(json.dumps(data, indent=2))

    # Also check if there are ANY students in Batch 10
    data_all = get_students_for_batch(db, batch_id=10, month=3, year=2025)
    print("\nAll Students in Batch 10:")
    print(f"Count: {len(data_all)}")
    if data_all:
        print(f"First student: {data_all[0]['name']}")

finally:
    db.close()
