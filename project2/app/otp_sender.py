from dotenv import load_dotenv
import os
import string
import secrets
import resend

load_dotenv()

resend_api_key = os.getenv("RESEND_API_KEY")

if not resend_api_key:
    raise "Plz add resend api key from resend website"


def generate_otp(length=4):
    digits = string.digits
    return "".join(secrets.choice(digits) for _ in range(length))


def send_otp(email: str) -> str:
    otp = generate_otp()

    resend.Emails.send(
        {
            "from": "OTP Sender <onboarding@resend.dev>",
            "to": email,
            "subject": "Your OTP is here!",
            "html": f"<p>Your OTP is: <strong>{otp}</strong></p>",
        }
    )


if __name__ == "__main__":
    generate_otp()
