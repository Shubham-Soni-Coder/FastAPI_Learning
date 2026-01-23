from fastapi import Request


class NotAuthenticatedException(Exception):
    pass


def get_current_user(request: Request):
    if "auth" not in request.session:
        raise NotAuthenticatedException()
    return request.session["user_id"]
