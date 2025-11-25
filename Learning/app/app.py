from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from sqlmodel import SQLModel, create_engine, Session

from .model import User


engine = create_engine("sqlite:///database.db")

app = FastAPI()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/form")
def show_form():
    with open("templates/form.html", "r") as f:
        return HTMLResponse(f.read())


@app.post("/submit")
def submit(
    username: str = Form(...), userphone: int = Form(...), useraddress: str = Form(...)
):
    with Session(engine) as session:
        user = User(name=username, phone=userphone, address=useraddress)
        session.add(user)
        session.commit()
        session.refresh(user)
    return {"status": "saved", "id": user.id}


@app.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.exec(select(user)).all()
    return users
