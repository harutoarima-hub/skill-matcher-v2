from flask import Blueprint, jsonify, request
from .db import db
from .models import Job
# ▼▼▼ ここの関数名を正しいものに修正しました ▼▼▼
from .match import calculate_ai_match_score

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
    # ▼▼▼ ここのチェックを 'skills' から 'profile_text' に修正しました ▼▼▼
    if not data or 'profile_text' not in data:
        return jsonify({'error': 'No profile text provided'}), 400

    user_profile_text = data.get('profile_text', '')
    all_jobs = Job.query.all()
    results = []
    for job in all_jobs:
        # 新しいAIマッチングロジックを呼び出す
        score, reasons = calculate_ai_match_score(user_profile_text, job)
        
        if score > 0: # スコアが0より大きいものだけ表示
            results.append({
                'job': job.to_dict(),
                'score': score,
                'reasons': reasons
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'results': results})