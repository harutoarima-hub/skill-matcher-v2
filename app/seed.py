from .db import db
from .models import Job
import random

def seed_data():
    """データベースに初期データを投入する関数"""
    
    # Jobデータのみを削除
    db.session.query(Job).delete()
    
    # --- 多様な業種の求人データ ---
    jobs_to_add = [
        # 飲食
        Job(title='ホールスタッフ', sector='飲食', company='グルメレストラン東京', location='東京', min_salary=280, max_salary=350,
            required_skills=['接客経験', '基本的なPC操作'], required_qualifications=[], experience_years=1, 
            nice_to_have=['英語対応', 'ソムリエ資格']),
        # 販売
        Job(title='アパレル販売員', sector='販売', company='ファッション・スタイル', location='大阪', min_salary=300, max_salary=400,
            required_skills=['販売経験', '在庫管理'], required_qualifications=[], experience_years=2, 
            nice_to_have=['VMD経験']),
        # 介護
        Job(title='介護福祉士', sector='介護', company='ケアホーム・やすらぎ', location='福岡', min_salary=320, max_salary=420,
            required_skills=['身体介助', '生活援助'], required_qualifications=['介護福祉士'], experience_years=3, 
            nice_to_have=['普通自動車免許']),
        # 事務
        Job(title='一般事務', sector='事務', company='ABC商事', location='名古屋', min_salary=250, max_salary=320,
            required_skills=['Word', 'Excel', '電話対応'], required_qualifications=[], experience_years=0, 
            nice_to_have=['簿記3級']),
        # IT
        Job(title='ソフトウェアエンジニア', sector='IT', company='TechNext Inc.', location='リモート', min_salary=500, max_salary=800,
            required_skills=['Python', 'AWS', 'Docker'], required_qualifications=[], experience_years=3, 
            nice_to_have=['Go言語'])
    ]
    
    # Jobデータのみをデータベースセッションに追加
    db.session.add_all(jobs_to_add)
    
    # 変更をデータベースにコミット
    db.session.commit()
    print(f"{len(jobs_to_add)}件の多様な求人データを投入しました。")