import functools
from flask import request
from flask import Response
from typing import Optional
import jwt
import datetime
from tinydb import Query
from config import db_user

User = Query()

class Accuracy:
    KEY = "secret"
    ALGORITHM = "HS256"
    
    def __call__(self, func):
        return self.decentralization(func=func)
    
    def decentralization(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if request.authorization.type == 'bearer' and request.authorization.token:
                    token = request.authorization.token
                    data = self.decode_jwt(token)
                    if func.__name__ in ["login"]:
                        if data:
                            kwargs['token'] = token
                            kwargs['session'] = token
                        else:
                            kwargs['token'] = None
                            kwargs['session'] = None
                        result = func(*args, **kwargs)
                        return result
                    elif data:
                        result = func(*args, **kwargs)
                        return result  
            except:
                if func.__name__ in ["login"]:
                    kwargs['token'] = None
                    kwargs['session'] = None
                    result = func(*args, **kwargs)
                    return result
            return Response('{"data":false}', status=403, mimetype='application/json')

        return wrapper
    
    @classmethod
    def decode_jwt(cls, encoded:str=None):
        try:
            if encoded is None:
                raise
            return jwt.decode(encoded, cls.KEY, algorithms=cls.ALGORITHM)
        except:
            return None
        
    @classmethod
    def encode_jwt(cls, data:dict, seconds:int = 3600):
        data["exp"] = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
        return jwt.encode(data, cls.KEY, algorithm=cls.ALGORITHM)
    
    @classmethod
    def accuracy(cls, data):
        username = data.get("username", None)
        password = data.get("password", None)
        if username and password:
            data_query = db_user.search(User.username == username)
            _password = data_query[0].get("password")
            if _password == password:
                return cls.encode_jwt(data)
        return None