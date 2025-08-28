from flask import Flask, render_template
from .db import init_db, db
from .routes import api # routes.py から api をインポート
from .models import Job

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

 # ▼▼▼ このブロックを追加 ▼▼▼
    @app.route("/job/<int:job_id>")
    def job_detail_page(job_id):
        job = Job.query.get_or_404(job_id)
        return render_template("job_detail.html", job=job)

    return app