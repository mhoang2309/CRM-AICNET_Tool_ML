from .endpoints.auth import auth_api
from .endpoints.file import file_api
from flask import Flask

def routers(app:Flask):
    app.register_blueprint(auth_api, url_prefix="/api")
    app.register_blueprint(file_api, url_prefix="/api")
