from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.schemas import UserCreate, Usermodel
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db, Base, engine
from app.models import User, OTP
from passlib.context import CryptContext
import hashlib
from datetime import datetime, timedelta

app = FastAPI()

# Static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


# Templates
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/", name="login")
def show_form(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})


@app.get("/register", name="register")
def show_register_form(request: Request):
    return templates.TemplateResponse("register_page.html", {"request": request})


@app.post("/register", name="register")
def register_user(
    request: Request,
    usergmail: str = Form(...),
    db: Session = Depends(get_db),
):

    # check existing gmail
    existing = db.query(User).filter(User.gmail_id == usergmail).first()

    if existing:
        # delete data just for testing
        print("data is already exist")
        return templates.TemplateResponse(
            "register_page.html", {"request": request, "error": "Email already in use"}
        )

    from .otp_sender import send_otp

    send_otp(usergmail)

    return templates.TemplateResponse("otp_send_page.html", {"request": request})


@app.post("/login_success", name="login_success")
def show_login_success(
    request: Request, username: str = Form(...), password: str = Form(...)
):
    with open("data.txt", "w") as f:
        f.write(f"Username: {username}\nPassword: {password}")
    return templates.TemplateResponse("login_success.html", {"request": request})


@app.post("/otp_send", name="otp_send")
def otp_sender(request: Request, usergmail: str = Form(...), password: str = Form(...)):

    from .otp_sender import send_otp

    send_otp(usergmail)
    return templates.TemplateResponse("otp_send_page.html", {"request": request})


@app.post("/check_otp", name="check_otp")
def check_otp(
    request: Request,
    usergmail: str = Form(...),
    otp: str = Form(...),
    db: Session = Depends(get_db),
):
    from .otp_sender import check_otp as verify_otp

    is_valid = verify_otp(usergmail, otp)

    if not is_valid:
        return templates.TemplateResponse(
            "otp_send_page.html",
            {"request": request, "error": "Invalid or expired OTP"},
        )

    # Check if we need to register the user or if they are already registered
    # For now, we assume success
    return templates.TemplateResponse("login_success.html", {"request": request})
