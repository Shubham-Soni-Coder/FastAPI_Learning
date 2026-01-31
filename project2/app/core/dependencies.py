from fastapi import Request


class NotAuthenticatedException(Exception):
    pass


def get_current_user(request: Request):
    if "auth" not in request.session:
        raise NotAuthenticatedException()
    return request.session["user_id"]


class NotAuthorizedException(Exception):
    def __init__(self, role: str):
        self.role = role


def get_current_teacher(request: Request):
    if "auth" not in request.session:
        raise NotAuthenticatedException()
    role = request.session.get("role")
    if not role or role.lower() != "teacher":
        raise NotAuthorizedException(role="teacher")
    return request.session["user_id"]


def get_current_student(request: Request):
    if "auth" not in request.session:
        raise NotAuthenticatedException()
    if request.session.get("role") not in ["Student", "Admin"]:
        raise NotAuthorizedException(role="Student")
    return request.session["user_id"]
