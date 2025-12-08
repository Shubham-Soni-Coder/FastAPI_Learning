from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
def show_form():
    with open("template/login_page.html", "r") as f:
        return HTMLResponse(f.read())
