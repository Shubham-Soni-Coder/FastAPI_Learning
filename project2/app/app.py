"""
Main Application Module
=======================

This module initializes the FastAPI application and defines the route handlers.
It includes routes for authentication (login, register), dashboard views, and teacher functionalities.
"""

from fastapi import FastAPI, status, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.middleware import setup_middleware
from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.models import *  # Import all models to ensure they are registered with Base
from app.routers import attendance, auth, dashboard, teacher
from app.core.config import Settings


# load the data
JSON_DATA = Settings.JSON_DATA

app = FastAPI()

# make database
db = SessionLocal()

# Include Routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(teacher.router)
app.include_router(attendance.router)

# Static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


# Templates
templates = Jinja2Templates(directory="templates")


from app.core.dependencies import NotAuthenticatedException

# add security
setup_middleware(app)


@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return RedirectResponse(url="/static/images/favicon.ico")
