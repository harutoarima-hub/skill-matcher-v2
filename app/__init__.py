from flask import Flask, render_template
from .db import init_db, db
from .routes import api

def create_app():
    app = Flask(__name__)
    init_db(app)

    app.register_blueprint(api, url_prefix="/api")

    @app.route("/")
    def my_profile_page():
        return render_template("my.html")
   

    return app