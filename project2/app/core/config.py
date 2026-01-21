from dotenv import load_dotenv
import os

# from app.utils.json_loader import load_json

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    # Safety check: Stop the app if the key is missing
    if SECRET_KEY is None:
        raise ValueError("No SECRET_KEY found in .env file!")

    # load the data
    JSON_DATA: dict = load_json()


settings = Settings()
