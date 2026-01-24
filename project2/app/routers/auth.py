from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services import auth_service
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
