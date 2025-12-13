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
from app.otp_sender import send_otp, verify_otp
from starlette.middleware.sessions import SessionMiddleware
from passlib.context import CryptContext


app = FastAPI()

# Static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


# Templates
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    SessionMiddleware,
    secret_key="CHANGE_THIS_TO_A_LONG_RANDOM_SECRET",
    same_site="lax",
    https_only=False,  # True in production
)


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
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    # hash the password
    pwd_context = CryptContext(schemes=["argon2"])

    hashed_password = pwd_context.hash(password)

    # check existing gmail
    existing = db.query(User).filter(User.gmail_id == usergmail).first()

    if existing:
        # delete data just for testing
        print("data is already exist")
        hashed_password = None
        return templates.TemplateResponse(
            "register_page.html", {"request": request, "error": "Email already in use"}
        )

    send_otp(usergmail)
    request.session["gmail"] = usergmail
    request.session["password"] = hashed_password
    request.session["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return templates.TemplateResponse(
        "otp_send_page.html", {"request": request, "usergmail": usergmail}
    )


@app.post("/login_success", name="login_success")
def show_login_success(
    request: Request, username: str = Form(...), password: str = Form(...)
):
    with open("data.txt", "w") as f:
        f.write(f"Username: {username}\nPassword: {password}")
    return templates.TemplateResponse("login_success.html", {"request": request})


@app.post("/otp_send", name="otp_send")
def otp_sender(request: Request, usergmail: str = Form(...), password: str = Form(...)):

    send_otp(usergmail)

    request.session["gmail"] = usergmail  # This is a cookie for brower

    return templates.TemplateResponse("otp_send_page.html", {"request": request})


@app.post("/verify-otp", name="verify_otp")
def verify_otp_code(
    request: Request,
    otp: str = Form(...),
    db: Session = Depends(get_db),
):

    gmail = request.session.get("gmail")
    password = request.session.get("password")
    timestamp = request.session.get("time")

    if not gmail:
        print("Session expried error")
        return templates.TemplateResponse(
            "otp_send_page.html",
            {"request": request, "error": "Session expired. Try again."},
        )

    is_valid = verify_otp(gmail, otp)

    if not is_valid:
        print("Otp not match")
        return templates.TemplateResponse(
            "otp_send_page.html",
            {"request": request, "error": "Invalid or expired OTP"},
        )

    # store userdata in database
    # Just for tasking we give username = "Default"
    # secure the password

    user = User(username="Default", gmail_id=gmail, password=password)
    db.add(user)
    db.commit()
    print("Data sucessful added")
    return templates.TemplateResponse("login_success.html", {"request": request})
