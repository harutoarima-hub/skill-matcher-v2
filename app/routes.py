from flask import Blueprint, jsonify, request
from .db import db
from .models import Job
from .match import calculate_holistic_score

api = Blueprint("api", __name__)

@api.get("/jobs")
def list_jobs():
    return jsonify([j.to_dict() for j in Job.query.all()])

@api.post("/import/jobs")
def import_jobs():
    items = request.get_json(force=True)
    if not isinstance(items, list):
        return jsonify({"error":"list expected"}), 400
    # ... (この関数の内容は変更ありません)
    # ...
    db.session.commit()
    return jsonify({"created": len(items)}), 201

@api.route('/match/ad_hoc', methods=['POST'])
def ad_hoc_match():
    data = request.get_json(force=True)
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    candidate_data = {
        'skills': [skill.strip() for skill in data.get('skills', '').split(',') if skill.strip()],
        'qualifications': [q.strip() for q in data.get('qualifications', '').split(',') if q.strip()],
        'experience_years': int(data.get('experience_years', 0) or 0)
    }

    all_jobs = Job.query.all()
    results = []
    for job in all_jobs:
        score, reasons = calculate_holistic_score(candidate_data, job)
        
        if score > 0.1:
            results.append({
                'job': job.to_dict(),
                'score': score,
                'reasons': reasons
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'results': results})

