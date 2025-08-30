from flask import Blueprint, jsonify, request
from .db import db
from .models import Job
# ▼▼▼ インポートする関数名を、新しい2つの名前に修正しました ▼▼▼
from .match import extract_keywords_with_gemini, calculate_similarity_score

api = Blueprint("api", __name__)

@api.get("/jobs")
def list_jobs():
    return jsonify([j.to_dict() for j in Job.query.all()])


@api.route('/match/ad_hoc', methods=['POST'])
def ad_hoc_match():
    data = request.get_json(force=True)
    if not data or 'profile_text' not in data:
        return jsonify({'error': 'No profile text provided'}), 400

    user_profile_text = data.get('profile_text', '')

    user_keywords = extract_keywords_with_gemini(user_profile_text)
    
    # ▼▼▼ このprint文を追加 ▼▼▼
    print(f"--- Geminiが抽出したキーワード: {user_keywords} ---")

    all_jobs = Job.query.all()
    results = []
    for job in all_jobs:
        score, reasons = calculate_similarity_score(user_keywords, job)
        
        # ▼▼▼ このprint文を追加 ▼▼▼
        print(f"-> 求人'{job.title}'とのスコア: {score}")

        if score > 0.1:
            results.append({
                'job': job.to_dict(),
                'score': score,
                'reasons': reasons
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'results': results})

# app/routes.py


from .db import db
from app.seed import seed_data

@api.route("/init-database-manually")
def init_database_manually():
    """
    手動でデータベースを初期化するための特別なエンドポイント。
    """
    try:
        print("--- [MANUAL INIT] データベースの初期化を開始します ---")
        
        # init_db.py がやっていた処理をここで実行
        db.drop_all()
        db.create_all()
        seed_data()
        
        print("--- [MANUAL INIT] データベースの初期化が成功しました ---")
        return "データベースの初期化に成功しました。", 200
    except Exception as e:
        print(f"--- [MANUAL INIT] エラーが発生しました: {e} ---")
        return f"エラーが発生しました: {e}", 500