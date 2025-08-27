from flask import Flask, render_template
from .db import init_db, db
from .routes import api

def create_app():
    app = Flask(__name__)
    init_db(app)

    app.register_blueprint(api, url_prefix="/api")

    # ▼▼▼ トップページで情報入力画面(my.html)を表示するように変更 ▼▼▼
    @app.route("/")
    def my_profile_page():
        return render_template("my.html")

    @app.route("/jobs")
    def jobs_page():
        return render_template("jobs.html")

    # ▼▼▼ /candidates のルートを削除しました ▼▼▼

    @app.route("/match")
    def match_page():
        return render_template("match.html")

    return app