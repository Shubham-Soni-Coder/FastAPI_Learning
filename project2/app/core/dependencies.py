from fastapi import Request


class NotAuthenticatedException(Exception):
    pass


def get_current_user(request: Request):
    if "gmail" not in request.session:
        raise NotAuthenticatedException()
    return request.session["gmail"]
