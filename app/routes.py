from flask import Blueprint, jsonify, request
from .db import db
from .models import Job
# ▼▼▼ ここの関数名を正しいものに修正しました ▼▼▼
from .match import calculate_ai_match_score
from .match import extract_keywords_with_gemini, calculate_similarity_score


api = Blueprint("api", __name__)

@api.get("/jobs")
def list_jobs():
    return jsonify([j.to_dict() for j in Job.query.all()])

# /import/jobs は変更なし
@api.post("/import/jobs")
def import_jobs():
    # ... (この関数の内容は変更ありません) ...
    db.session.commit()
    return jsonify({"created": len(items)}), 201

@api.route('/match/ad_hoc', methods=['POST'])
def ad_hoc_match():
    data = request.get_json(force=True)
    if not data or 'profile_text' not in data:
        return jsonify({'error': 'No profile text provided'}), 400

    user_profile_text = data.get('profile_text', '')

    # ▼▼▼ ループの前に、一度だけAPIを呼び出す ▼▼▼
    user_keywords = extract_keywords_with_gemini(user_profile_text)

    all_jobs = Job.query.all()
    results = []
    for job in all_jobs:
        # ▼▼▼ APIを呼び出さないスコア計算関数を使用 ▼▼▼
        score, reasons = calculate_similarity_score(user_keywords, job)
        
        if score > 0:
            results.append({
                'job': job.to_dict(),
                'score': score,
                'reasons': reasons
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'results': results})