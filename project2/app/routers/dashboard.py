from fastapi import APIRouter, Request, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.core.dependencies import get_current_user


# Initialize templates
templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/dashboard", name="dashboard")
def show_dashboard(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request})
