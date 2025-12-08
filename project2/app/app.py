from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/styles", StaticFiles(directory="styles"), name="styles")
app.mount("/images", StaticFiles(directory="images"), name="images")

# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/")
def show_form(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})
