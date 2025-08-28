from flask import Flask, render_template
from .db import init_db, db
from .routes import api # routes.py から api をインポート

def create_app():
    app = Flask(__name__)
    init_db(app)

    # ▼▼▼ この一行を追加して、APIの設計図をアプリに登録します ▼▼▼
    app.register_blueprint(api, url_prefix="/api")

    @app.route("/")
    def my_profile_page():
        return render_template("my.html")

    @app.route("/jobs")
    def jobs_page():
        return render_template("jobs.html")

    return app