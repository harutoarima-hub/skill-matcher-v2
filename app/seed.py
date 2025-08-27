# app/seed.py

from .db import db
from .models import Job, Candidate

def seed_data():
    """データベースに初期データを投入する関数"""
    
    db.session.query(Candidate).delete()
    db.session.query(Job).delete()
    
    # サンプルの求人データ
    job1 = Job(
        title='バックエンドエンジニア', 
        company='株式会社Render', 
        location='東京', 
        min_salary=500, 
        max_salary=800, 
        employment_type='正社員'
        # required_skills の行を削除しました
    )
    job2 = Job(
        title='フロントエンドエンジニア', 
        company='株式会社Render', 
        location='大阪', 
        min_salary=450, 
        max_salary=700, 
        employment_type='正社員'
        # required_skills の行を削除しました
    )

    # サンプルの候補者データ
    candidate1 = Candidate(
        name='山田 太郎', 
        skills=['Python', 'Flask', 'Docker']
    )
    candidate2 = Candidate(
        name='鈴木 花子', 
        skills=['JavaScript', 'React', 'TypeScript', 'CSS']
    )
    
    db.session.add(job1)
    db.session.add(job2)
    db.session.add(candidate1)
    db.session.add(candidate2)
    
    db.session.commit()
    print("データベースへのデータ投入が完了しました。")