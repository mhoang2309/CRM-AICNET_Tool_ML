from flask import Blueprint
from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
from ..render import render_template as my_render_template
from ..cookie import Cookie

home = Blueprint('home', __name__)

@home.get("")
@Cookie()
def index():
    return render_template('home.html')

@home.get("login")
@Cookie()
def login():
    _body = render_template("login.html")
    return my_render_template(link=["login"], title="Login", body=_body, script=["login"])