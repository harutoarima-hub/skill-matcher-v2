import traceback
from app import create_app, db
from app.seed import seed_data

print("--- [START] データベース初期化スクリプト ---")

try:
    app = create_app()
    with app.app_context():
        print(" -> テーブルを作成しています...")
        db.create_all()
        
        print(" -> 初期データを投入しています...")
        seed_data()

    print("--- [SUCCESS] データベースの初期化が完了しました ---")

except Exception as e:
    print("--- [ERROR] データベース初期化中にエラーが発生しました ---")
    traceback.print_exc()
    print("----------------------------------------------------")