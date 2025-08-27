from flask import Flask, render_template
from .db import init_db, db
from .routes import api

def create_app():
    app = Flask(__name__)
    init_db(app)

    app.register_blueprint(api, url_prefix="/api")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/jobs")
    def jobs_page():
        return render_template("jobs.html")

    @app.route("/candidates")
    def candidates_page():
        return render_template("candidates.html")

    @app.route("/match")
    def match_page():
        return render_template("match.html")
    
    @app.route("/my-profile")
    def my_profile_page():
        return render_template("my.html")

    return app