# app/__init__.py

from flask import Flask, render_template
from .db import init_db, db
from .routes import api
from .seed import seed_data  # ★★★ seed.pyから関数をインポート ★★★

def create_app():
    # ... (この部分は変更なし) ...
    return app

app = create_app()

@app.cli.command("init-db")
def init_db_command():
    """データベースのテーブルを作成し、初期データを投入します。"""
    with app.app_context():
        db.create_all()      # 1. テーブルを作成
        seed_data()          # 2. データを投入
    print("データベースの初期化とデータ投入が完了しました。")