from .db import db
from .models import Job, Candidate # app/models.py で定義したモデルをインポート

# 全てのロジックをこの関数の中に移動します
def seed_data():
    """データベースに初期データを投入する関数"""
    
    # 既存のデータを全て削除（開発用に便利です）
    db.session.query(Candidate).delete()
    db.session.query(Job).delete()
    
    # --- ここに投入したいサンプルデータを記述します ---

    # サンプルの求人データ
    job1 = Job(
        title='バックエンドエンジニア', 
        company='株式会社Render', 
        location='東京', 
        min_salary=500, 
        max_salary=800, 
        employment_type='正社員', 
        required_skills='Python,Flask,SQL'
    )
    job2 = Job(
        title='フロントエンドエンジニア', 
        company='株式会社Render', 
        location='大阪', 
        min_salary=450, 
        max_salary=700, 
        employment_type='正社員', 
        required_skills='JavaScript,React,CSS'
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
    
    # -------------------------------------------

    # データベースセッションに追加
    db.session.add(job1)
    db.session.add(job2)
    db.session.add(candidate1)
    db.session.add(candidate2)
    
    # 変更をデータベースにコミット
    db.session.commit()
    print("データベースへのデータ投入が完了しました。")