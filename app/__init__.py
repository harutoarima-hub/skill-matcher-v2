from flask import Flask, render_template
from .db import init_db
from .routes import api

def create_app():
    app = Flask(__name__)
    init_db(app)  # DB作成・初期化

    # API
    app.register_blueprint(api, url_prefix="/api")

    # 画面（最低限）
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

    return app

app = create_app()
