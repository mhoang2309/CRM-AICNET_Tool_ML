from flask import Flask
from api.routers import routers as routers_api
from web.routers import routers as routers_web


app = Flask(__name__, template_folder="./static/template", static_url_path="")

routers_api(app)
routers_web(app)

if __name__ == '__main__':
    app.run(debug=True)


