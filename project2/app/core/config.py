from dotenv import load_dotenv
import os

from app.utils.json_loader import load_json

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY")
    # Safety check: Stop the app if the key is missing
    if SECRET_KEY is None:
        raise ValueError("No SECRET_KEY found in .env file!")
    if DATABASE_URL is None:
        raise ValueError("No DATABASE_URL found in .env file!")
    if RESEND_API_KEY is None:
        raise ValueError("No RESEND_API_KEY found in .env file!")

    # load the data
    JSON_DATA: dict = load_json()


settings = Settings()
