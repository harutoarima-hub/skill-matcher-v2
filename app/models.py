from .db import db
from sqlalchemy.types import JSON

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(50))
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    min_salary = db.Column(db.Integer)
    max_salary = db.Column(db.Integer)
    
    # ▼▼▼ 詳細な情報を保存できるよう、Text型とJSON型に更新 ▼▼▼
    description = db.Column(db.Text)          # 仕事内容 (長い文章)
    requirements = db.Column(db.Text)         # 必須要件 (長い文章)
    welcome_requirements = db.Column(db.Text) # 歓迎要件 (長い文章)
    
    # AIで抽出しやすいように、キーワードも別途保存
    keywords = db.Column(db.JSON)             # 例: ["Python", "AWS", "リーダーシップ"]

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'sector': self.sector,
            'company': self.company,
            'location': self.location,
            'min_salary': self.min_salary,
            'max_salary': self.max_salary,
            'description': self.description,
            'requirements': self.requirements,
            'welcome_requirements': self.welcome_requirements,
            'keywords': self.keywords or []
        }

# ▼▼▼ ユーザー情報を扱うための新しいモデル（テーブル）を追加 ▼▼▼
# (今回は使用しませんが、将来的な拡張のために定義しておきます)
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # 自由な形式のデータをJSONで保存する
    profile_data = db.Column(db.JSON)
    # AIによって抽出・正規化されたキーワード
    keywords = db.Column(db.JSON)