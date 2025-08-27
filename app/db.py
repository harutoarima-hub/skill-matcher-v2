# app/db.py の最終版の全コード

from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    # 環境変数からデータベースURLを取得
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # アプリケーションコンテキスト内でモデルをインポートし、テーブルを作成
    with app.app_context():
     
        from .models import Job 
        db.create_all()