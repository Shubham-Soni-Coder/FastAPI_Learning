import json
import sys
import os

# Add current directory to path so we can import app
sys.path.append(os.getcwd())

try:
    from app.core.security import hash_password
except ImportError:
    # Fallback if app.core.security is not found or dependencies missing
    # We will try to use passlib directly if installed, or just placeholder
    print(
        "Could not import hash_password from app.core.security, trying direct passlib"
    )
    try:
        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        def hash_password(password: str):
            return pwd_context.hash(password)

    except ImportError:
        print(
            "Could not import passlib. using valid placeholder hash but this won't work for login if backend verifies hash"
        )

        def hash_password(password: str):
            return f"hashed_{password}"


def fix_data():
    file_path = "data.json"
    with open(file_path, "r") as f:
        data = json.load(f)

    students = data.get("students", [])

    # Password that meets criteria: At least 8 chars, 1 upper, 1 lower, 1 number, 1 special
    # "Student@123" -> S(upper), t(lower), @(special), 1(number), length 11.
    new_password_plain = "Student@123"
    new_password_hash = hash_password(new_password_plain)

    print(f"Updating passwords to hash of '{new_password_plain}'")

    for student in students:
        name = student.get("name", "").strip()
        roll_no = student.get("roll_no", "")
        email = student.get("email", "")

        # 1. Fix Email if it is a placeholder/demo
        # Logic: If email contains 'demo' or doesn't seem to contain the name (case insensitive)
        if "demo" in email.lower() or name.lower().split()[0] not in email.lower():
            # Construct new email: FirstName + RollNoLast2Digits + @gmail.com
            first_name = name.split()[0]
            # remove spaces from first name just in case
            first_name = first_name.replace(" ", "")

            suffix = roll_no[-2:] if len(roll_no) >= 2 else roll_no
            new_email = f"{first_name}{suffix}@gmail.com"
            student["email"] = new_email
            print(f"Updated email for {name} ({roll_no}) to {new_email}")

        # 2. Fix Password
        # Update ALL students to the new strong password hash
        student["hashed_password"] = new_password_hash

    data["students"] = students

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    print("data.json updated successfully.")


if __name__ == "__main__":
    fix_data()
