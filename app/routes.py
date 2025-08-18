from flask import Blueprint, jsonify, request
from .db import db
from .models import Job, Candidate
from .match import rank_for_job

api = Blueprint("api", __name__)

@api.get("/jobs")
def list_jobs():
    return jsonify([_job_to_dict(j) for j in Job.query.all()])

@api.post("/import/jobs")
def import_jobs():
    items = request.get_json(force=True)
    if not isinstance(items, list):
        return jsonify({"error":"list expected"}), 400
    for it in items:
        j = Job(
            title=it.get("title",""),
            company=it.get("company",""),
            must_have_skills=it.get("must_have_skills",[]),
            nice_to_have_skills=it.get("nice_to_have_skills",[]),
            location=it.get("location","Tokyo"),
            min_salary=int(it.get("min_salary",0) or 0),
            max_salary=int(it.get("max_salary",0) or 0),
            employment_type=it.get("employment_type","Full-time"),
            description=it.get("description",""),
            salary=it.get("salary")
        )
        db.session.add(j)
    db.session.commit()
    return jsonify({"created": len(items)}), 201

@api.get("/candidates")
def list_candidates():
    return jsonify([_cand_to_dict(c) for c in Candidate.query.all()])

@api.post("/import/candidates")
def import_candidates():
    items = request.get_json(force=True)
    if not isinstance(items, list):
        return jsonify({"error":"list expected"}), 400
    for it in items:
        c = Candidate(
            name=it.get("name",""),
            skills=it.get("skills",[]),
            years=int(it.get("years",0) or 0),
            desired_location=it.get("desired_location","Tokyo"),
            desired_min_salary=int(it.get("desired_min_salary",0) or 0),
            availability=it.get("availability","immediate")
        )
        db.session.add(c)
    db.session.commit()
    return jsonify({"created": len(items)}), 201

@api.get("/match")
def match_for_job():
    job_id = request.args.get("job_id", type=int)
    if not job_id:
        return jsonify({"error":"job_id is required"}), 400
    job = Job.query.get_or_404(job_id)
    ranked = rank_for_job(job, Candidate.query.all())
    return jsonify({"job": _job_to_dict(job), "results": ranked})

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
# ---- delete all candidates (bulk) ----
from sqlalchemy import delete
@api.delete("/candidates")
def delete_all_candidates():
    db.session.execute(delete(Candidate))
    db.session.commit()
    return ("", 204)
# ---- rename candidates sequentially (Aさん〜Tさん) ----
@api.post("/candidates/rename_sequential")
def rename_candidates_sequential():
    names = ["Aさん","Bさん","Cさん","Dさん","Eさん","Fさん","Gさん","Hさん","Iさん","Jさん","Kさん","Lさん","Mさん","Nさん","Oさん","Pさん","Qさん","Rさん","Sさん","Tさん"]
    cands = Candidate.query.order_by(Candidate.id.asc()).all()
    for i, c in enumerate(cands):
        c.name = names[i] if i < len(names) else f"候補者{i+1}"
    db.session.commit()
    return jsonify({"renamed": min(len(cands), len(names)), "total": len(cands)})
