from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# Initialize templates
templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/dashboard", name="dashboard")
def show_dashboard(request: Request):
    # Security check: exist session
    if "gmail" not in request.session:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("dashboard.html", {"request": request})
