import json
from flask import Blueprint, request, make_response
from werkzeug.utils import secure_filename
import os
from ..functions.accuracy import Accuracy
from flask import Response
from ..functions.service import new_user

auth_api = Blueprint('auth_api', __name__)


@auth_api.post("login")
@Accuracy()
def login(token, session):
    res = Response
    if token:
        data = {"login": True,
                "authorization": token}
        res = res(json.dumps(data), status=200, mimetype='application/json')
        res.set_cookie("_authorization", value=token)
        res.set_cookie("_session", value=session)
        return res
    try:
        _token = Accuracy.accuracy(request.json)
        if _token:
            data = {"login": True,
                "authorization": _token}
            res = res(json.dumps(data), status=200, mimetype='application/json')
            res.set_cookie("_authorization", value=_token)
            res.set_cookie("_session", value=_token)
            return res
        return res('{"login": false}', status=403, mimetype='application/json')
    except:
        res = res('{"login": false}', status=500, mimetype='application/json')
        res.delete_cookie("_authorization")
        res.delete_cookie("_session")
        return res

@auth_api.get("logout")
def logout():
    pass

@auth_api.get("infor")
@Accuracy()
def infor():
    pass

@auth_api.put("signup")
def signup():
    try:
        data = request.json
        username = data.get("username", None)
        code = data.get("code", None)
        password = data.get("password", None)
        if username and code and password:
            if new_user(username, code, password):
                return Response(json.dumps({"signup":True}), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({"signup":False}), status=401, mimetype='application/json')
    except:
        return Response(json.dumps({"signup":False}), status=500, mimetype='application/json')
    