from .db import db
from sqlalchemy.types import JSON
from sqlalchemy import Text

class Job(db.Model):
    __tablename__ = "job"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), default='')
    # 互換のため salary も定義（古い参照が残っても落ちないように）
    salary = db.Column(db.String(255))
    must_have_skills = db.Column(JSON, default=list)
    nice_to_have_skills = db.Column(JSON, default=list)
    location = db.Column(db.String(255))
    min_salary = db.Column(db.Integer, default=0)
    max_salary = db.Column(db.Integer, default=0)
    employment_type = db.Column(db.String(40), default='Full-time')
    description = db.Column(Text, default='')

class Candidate(db.Model):
    __tablename__ = "candidate"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    skills = db.Column(JSON, default=list)
    years = db.Column(db.Integer, default=0)
    desired_location = db.Column(db.String(80), default='Tokyo')
    desired_min_salary = db.Column(db.Integer, default=0)
    availability = db.Column(db.String(40), default='immediate')
