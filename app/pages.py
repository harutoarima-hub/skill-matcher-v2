from flask import Blueprint, render_template, request, abort
from .models import Job, Candidate
from .match import rank_for_job

pages = Blueprint("pages", __name__)

@pages.get("/job")
def job_page():
    jobs = Job.query.order_by(Job.id.asc()).all()
    return render_template("jobs.html", jobs=jobs)

@pages.get("/match")
def match_page():
    job_id = request.args.get("job_id", type=int)
    if not job_id:
        jobs = Job.query.order_by(Job.id.asc()).all()
        return render_template("match.html", jobs=jobs, matches=[])
    job = Job.query.get(job_id)
    if not job:
        abort(404)
    ranked = rank_for_job(job, Candidate.query.all())
    return render_template("match.html", job=job, matches=ranked)
