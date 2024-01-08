import functools
from flask import request
from flask import redirect
from api.functions.accuracy import Accuracy


class Cookie:
    def __init__(self):
        pass
    def __call__(self, func) :
        return self.check_session(func=func)
    
    def check_session(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            token = request.cookies.get("_authorization", None)
            session = request.cookies.get("_session", None)
            _token = Accuracy.decode_jwt(token)
            _session = Accuracy.decode_jwt(session)
            if _token and _session:
                if func.__name__=="login":
                    return redirect("/", code=302)
                result = func(*args, **kwargs)
                return result
            else:
                if func.__name__=="login":
                    result = func(*args, **kwargs)
                    return result
                return redirect("/login", code=302)

        return wrapper