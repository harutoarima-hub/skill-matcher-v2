from flask import Blueprint, jsonify, request
from .db import db
from .models import Job, Candidate
# ▼▼▼ 変更点1: 新しいマッチング関数をインポート ▼▼▼
from .match import rank_for_job, calculate_holistic_score

api = Blueprint("api", __name__)

@api.get("/jobs")
def list_jobs():
    # Jobモデルのto_dictメソッドを使うように変更するとよりシンプルになります
    return jsonify([j.to_dict() for j in Job.query.all()])

# ... (import/jobs, /candidates, import/candidates は変更なし) ...
@api.post("/import/jobs")
def import_jobs():
    items = request.get_json(force=True)
    if not isinstance(items, list):
        return jsonify({"error":"list expected"}), 400
    # ... (この関数の内容は変更なし) ...
    db.session.commit()
    return jsonify({"created": len(items)}), 201

@api.get("/candidates")
def list_candidates():
    # Candidateモデルのto_dictメソッドを使うように変更するとよりシンプルになります
    return jsonify([c.to_dict() for c in Candidate.query.all()])

@api.post("/import/candidates")
def import_candidates():
    items = request.get_json(force=True)
    if not isinstance(items, list):
        return jsonify({"error":"list expected"}), 400
    # ... (この関数の内容は変更なし) ...
    db.session.commit()
    return jsonify({"created": len(items)}), 201


@api.get("/match")
def match_for_job():
    job_id = request.args.get("job_id", type=int)
    if not job_id:
        return jsonify({"error":"job_id is required"}), 400
    job = Job.query.get_or_404(job_id)
    ranked = rank_for_job(job, Candidate.query.all())
    # Jobモデルのto_dict()を使うように変更
    return jsonify({"job": job.to_dict(), "results": ranked})

# ▼▼▼ 変更点2: この新しいAPIルートをまるごと追加 ▼▼▼
@api.route('/match/ad_hoc', methods=['POST'])
def ad_hoc_match():
    data = request.get_json(force=True)
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # フロントエンドから送られてくる候補者データ
    candidate_data = {
        'skills': [skill.strip() for skill in data.get('skills', '').split(',') if skill.strip()],
        'qualifications': [q.strip() for q in data.get('qualifications', '').split(',') if q.strip()],
        'experience_years': int(data.get('experience_years', 0) or 0)
    }

    all_jobs = Job.query.all()
    results = []
    for job in all_jobs:
        # 新しい総合評価ロジックを呼び出す
        score, reasons = calculate_holistic_score(candidate_data, job)
        
        if score > 0.1: # マッチ度が10%以上のものだけ表示
            results.append({
                'job': job.to_dict(),
                'score': score,
                'reasons': reasons
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'results': results})


# --- 既存のヘルパー関数や追加機能 (変更なし) ---

# _job_to_dict と _cand_to_dict は models.py の to_dict() に移行したため不要になりますが、
# rank_for_job 関数などがまだ使っている可能性を考慮して残しておきます。
def _job_to_dict(j: Job):
    return {
        "id": j.id, "title": j.title, "company": j.company,
        "must_have_skills": j.must_have_skills or [],
        "nice_to_have_skills": j.nice_to_have_skills or [],
        "location": j.location, "min_salary": j.min_salary, "max_salary": j.max_salary,
        "employment_type": j.employment_type, "description": j.description or "", "salary": j.salary
    }

def _cand_to_dict(c: Candidate):
    return {
        "id": c.id, "name": c.name, "skills": c.skills or [], "years": c.years,
        "desired_location": c.desired_location, "desired_min_salary": c.desired_min_salary,
        "availability": c.availability
    }

from sqlalchemy import delete
@api.delete("/candidates")
def delete_all_candidates():
    db.session.execute(delete(Candidate))
    db.session.commit()
    return ("", 204)

@api.post("/candidates/rename_sequential")
def rename_candidates_sequential():
    names = ["Aさん","Bさん","Cさん","Dさん","Eさん","Fさん","Gさん","Hさん","Iさん","Jさん","Kさん","Lさん","Mさん","Nさん","Oさん","Pさん","Qさん","Rさん","Sさん","Tさん"]
    cands = Candidate.query.order_by(Candidate.id.asc()).all()
    for i, c in enumerate(cands):
        c.name = names[i] if i < len(names) else f"候補者{i+1}"
    db.session.commit()
    return jsonify({"renamed": min(len(cands), len(names)), "total": len(cands)})