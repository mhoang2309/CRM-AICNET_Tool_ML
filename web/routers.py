from .home import home
from flask import Flask

def routers(app:Flask):
    app.register_blueprint(home, url_prefix="/")
