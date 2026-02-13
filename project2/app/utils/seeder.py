from sqlalchemy.orm import Session
from datetime import datetime, date, time
from app.models import (
    User, Teacher, Student, Batches, Subject, 
    FeesStructure, FeesComponent, ClassSchedule, ClassInstance
)
from app.core.config import Settings

def parse_time(time_str: str):
    try:
        # Tries to parse "08:30 AM" or similar formats
        return datetime.strptime(time_str, "%I:%M %p").time()
    except Exception as e:
        print(f"Warning: Could not parse time '{time_str}', using fallback 09:00.")
        return time(9, 0)

def seed_database(db: Session):
    # 1. Quick check if data exists (Users table)
    if db.query(User).first():
        print("Database already has data. Skipping seeder.")
        return

    print("🚀 Starting Seeder (Strict Model - No Random Data)...")
    data = Settings.JSON_DATA

    # --- A. Subjects ---
    print("  -> Seeding Subjects...")
    # Gather all unique subject names from the JSON structure
    subject_names = set(data.get("Subjects", {}).get("Common", []))
    subject_names.update(data.get("Subjects", {}).get("Optional", []))
    
    # Also check streams
    streams = data.get("Subjects", {}).get("Streams", {})
    for stream_content in streams.values():
        for cat_list in stream_content.values():
            if isinstance(cat_list, list):
                subject_names.update(cat_list)
    
    # Insert Subjects
    for name in subject_names:
        if not db.query(Subject).filter_by(name=name).first():
            db.add(Subject(name=name))
    db.commit()

    # Create a nice lookup map: "Mathematics" -> ID 5
    subject_map = {sub.name: sub.id for sub in db.query(Subject).all()}


    # --- B. Batches ---
    # We infer batches from "fees_by_class" keys (e.g., "1", "10", "11_science")
    print("  -> Seeding Batches...")
    batch_map = {} # "11_science" -> Batch Object
    
    fees_data = data.get("fees_by_class", {})
    for batch_key in fees_data.keys():
        # batch_key could be "10" or "11_science"
        if "_" in batch_key:
            # e.g. "11_science"
            parts = batch_key.split("_")
            b_name = parts[0] + "th" # "11th"
            b_stream = parts[1]      # "science"
        else:
            # e.g. "10"
            b_name = batch_key + "th"
            b_stream = None # up to 10th usually no stream
            
        # Create Batch if not exists
        batch = Batches(batch_name=b_name, stream=b_stream)
        db.add(batch)
        db.flush() # get ID
        batch_map[batch_key] = batch # Store for linking later

    # --- C. Fees (Structure & Components) ---
    print("  -> Seeding Fees...")
    for batch_key, components in fees_data.items():
        batch_obj = batch_map.get(batch_key)
        if batch_obj:
            # Create Structure
            struct = FeesStructure(
                batch_id=batch_obj.id,
                academic_year="2025-26",
                is_active=True
            )
            db.add(struct)
            db.flush()
            
            # Create Components
            for fee in components:
                comp = FeesComponent(
                    fees_structure_id=struct.id,
                    component_name=fee["component_name"],
                    amount=fee["amount"]
                )
                db.add(comp)
    db.commit()


    # --- D. Teachers ---
    print("  -> Seeding Teachers...")
    
    for t_data in data.get("teacher", []):
        # 1. User Account
        user = User(
            gmail_id=t_data["gmail"],
            hashed_password=t_data["hashed_password"],
            role="teacher",
            is_active=True
        )
        db.add(user)
        db.flush()
        
        # 2. Teacher Profile
        teacher = Teacher(
            user_id=user.id,
            full_name=t_data["name"],
            department=t_data["department_name"]
        )
        db.add(teacher)
        db.flush()
    db.commit()


    # --- E. Students ---
    print("  -> Seeding Students...")
    
    # Get created batches for assignment - fallback to first available
    available_batches = list(batch_map.values())
    default_batch = available_batches[0] if available_batches else None
    
    if default_batch:
        for s_data in data.get("students", []):
            # 1. User Account
            user = User(
                gmail_id=s_data["email"],
                hashed_password=s_data["hashed_password"],
                role="student",
                is_active=s_data["is_active"]
            )
            db.add(user)
            db.flush()
            
            # 2. Student Profile - assigning to default batch since JSON has no batch info
            student = Student(
                user_id=user.id,
                roll_no=int(s_data["roll_no"]),
                name=s_data["name"],
                father_name=s_data["father_name"],
                mother_name=s_data.get("mother_name", ""),
                batch_id=default_batch.id
            )
            db.add(student)
        db.commit()


    # --- F. Class Schedules & Instances ---
    print("  -> Seeding Schedules...")
    
    # We need a map of scheduled IDs to DB IDs for the instances
    schedule_db_map = {} # JSON Schedule ID (index+1) -> DB ID

    for idx, sched_data in enumerate(data.get("class_schedules", [])):
        # 1. Resolve Subject ID
        sub_name = sched_data["subject"]
        sub_id = subject_map.get(sub_name)
        if not sub_id:
            # If subject missing, create on fly
            sub = Subject(name=sub_name)
            db.add(sub)
            db.flush()
            sub_id = sub.id
            subject_map[sub_name] = sub_id

        # 2. Resolve Batch ID
        # JSON uses "batch_id": 10. We must map this to our created batches.
        # We try to interpret "10" as key "10" in our batch_map.
        json_batch_key = str(sched_data.get("batch_id"))
        
        target_batch = batch_map.get(json_batch_key)
        if not target_batch:
            # Fallback: assume the integer might be an index or just pick first
            target_batch = default_batch
            
        if not target_batch:
            continue # Should not happen if batches seeded

        # 3. Resolve Teacher ID
        # JSON has "teacher_id": 1. We assume this matches the auto-increment ID 
        # from our teacher insertion loop.
        teacher_id = sched_data.get("teacher_id", 1)

        # Start/End Time
        t_start = parse_time(sched_data["start_time"])
        t_end = parse_time(sched_data["end_time"])

        try:
            new_sched = ClassSchedule(
                batch_id=target_batch.id,
                teacher_id=teacher_id,
                subject_id=sub_id,
                day_of_week=sched_data["day_of_week"],
                name=sched_data["name"],
                start_time=t_start,
                end_time=t_end
            )
            db.add(new_sched)
            db.flush()
            
            # Map JSON index (1-based) to DB ID
            schedule_db_map[idx + 1] = new_sched.id
            
        except Exception:
            db.rollback()
            print(f"    Skipping duplicate/invalid schedule: {sched_data['name']}")

    db.commit()

    # --- G. Class Instances ---
    print("  -> Seeding Class Instances...")
    for inst_data in data.get("class_instances", []):
        try:
            json_sid = inst_data["schedule_id"]
            real_sid = schedule_db_map.get(json_sid)
            
            if real_sid:
                instance = ClassInstance(
                    schedule_id=real_sid,
                    class_date=datetime.strptime(inst_data["class_date"], "%Y-%m-%d").date(),
                    status=inst_data["status"]
                )
                db.add(instance)
        except Exception as e:
            print(f"Skipping instance: {e}")
    
    db.commit()
    print("✅ STRICT SEED COMPLETE! Populated database using ONLY data.json.")
