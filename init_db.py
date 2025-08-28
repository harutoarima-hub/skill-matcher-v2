# init_db.py

import traceback
from app import create_app, db

print("--- [START] データベース初期化スクリプト ---")

try:
    app = create_app()
    with app.app_context():
        # アプリの準備が整った後で seed_data をインポートします
        from app.seed import seed_data

        print(" -> [!!!] 既存のテーブルを全て削除します...")
        db.drop_all()  # ← この行を追加

        print(" -> 新しい設計でテーブルを作成しています...")
        db.create_all()  # ← この行で新しいテーブルが作られる

        print(" -> 初期データを投入しています...")
        seed_data()

    print("--- [SUCCESS] データベースの初期化が完了しました ---")

except Exception as e:
    print("--- [ERROR] データベース初期化中にエラーが発生しました ---")
    traceback.print_exc()
    print("----------------------------------------------------")