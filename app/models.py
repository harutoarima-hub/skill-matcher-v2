from .db import db
from sqlalchemy.types import JSON

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(50)) # 業種
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    min_salary = db.Column(db.Integer)
    max_salary = db.Column(db.Integer)
    
    # 評価項目を柔軟なJSON形式に変更
    required_skills = db.Column(db.JSON)      # 必須スキル・経験
    required_qualifications = db.Column(db.JSON) # 必須資格
    experience_years = db.Column(db.Integer, default=0) # 必須経験年数
    nice_to_have = db.Column(db.JSON)         # あれば歓迎される項目

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'sector': self.sector,
            'company': self.company, 'location': self.location,
            'min_salary': self.min_salary, 'max_salary': self.max_salary,
            'required_skills': self.required_skills or [],
            'required_qualifications': self.required_qualifications or [],
            'experience_years': self.experience_years,
            'nice_to_have': self.nice_to_have or [],
        }