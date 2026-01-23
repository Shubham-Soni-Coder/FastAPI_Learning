from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services import auth_service, otp_service
from app.core.exceptions import CustomException

# Initialize templates
templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", name="login_page")
def show_form(request: Request):
    # Security check: exist session
    if "auth" in request.session:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login_page.html", {"request": request})


@router.get("/register", name="register")
def show_register_form(request: Request):
    return templates.TemplateResponse("register_page.html", {"request": request})


@router.post("/register", name="register")
def register_user(
    request: Request,
    usergmail: str = Form(...),
    userpassword: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        auth_service.start_register(db, usergmail, userpassword, request.session)
    except CustomException as e:
        return templates.TemplateResponse(
            "register_page.html", {"request": request, "error": e.detail}
        )

    return templates.TemplateResponse(
        "otp_send_page.html", {"request": request, "usergmail": usergmail}
    )


@router.post("/login", name="login")
def login(
    request: Request,
    usergmail: str = Form(...),
    userpassword: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user = auth_service.login_user(db, usergmail, userpassword, request.session)

        # Save user info in session
        request.session["user_id"] = user.id
        request.session["role"] = user.role
        request.session["auth"] = True

        # Redirect based on role
        if user.role == "teacher":
            return RedirectResponse(
                url="/teacher/dashboard", status_code=status.HTTP_303_SEE_OTHER
            )
        elif user.role == "Student":  # Matching the case from your create_user script
            return RedirectResponse(
                url="/dashboard", status_code=status.HTTP_303_SEE_OTHER
            )
        elif user.role == "Admin":
            return RedirectResponse(
                url="/dashboard", status_code=status.HTTP_303_SEE_OTHER
            )

        # Default fallback
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    except CustomException as e:
        return templates.TemplateResponse(
            "login_page.html",
            {"request": request, "error": e.detail},
        )


@router.post("/login_success", name="login_success")
def show_login_success(
    request: Request,
):
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logout", name="logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/otp_send", name="otp_send")
def otp_sender(
    request: Request,
    usergmail: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    # We pass 'db' here because send_otp now requires it
    otp_service.send_otp(usergmail, db)

    request.session["gmail"] = usergmail
    return templates.TemplateResponse("otp_send_page.html", {"request": request})


@router.post("/verify-otp", name="verify_otp")
def verify_otp_code(
    request: Request,
    otp: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        auth_service.complet_register(db, request.session, otp)
        print("Data sucessful added")
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    except CustomException as e:
        return templates.TemplateResponse(
            "otp_send_page.html",
            {"request": request, "error": e.detail},
        )
