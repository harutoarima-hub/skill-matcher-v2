from .db import db
from .models import Job, Candidate

def seed_data():
    db.session.query(Candidate).delete()
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

    # --- 多様なスキルセットを持つ候補者データ ---
    candidates_to_add = [
        Candidate(name='佐藤 圭介', skills=['接客経験', '英語対応', 'ソムリエ資格'], qualifications=['ソムリエ資格'], experience_years=5),
        Candidate(name='高橋 美咲', skills=['販売経験', 'VMD経験', '在庫管理'], qualifications=[], experience_years=3),
        Candidate(name='田中 誠', skills=['身体介助', '生活援助', 'レクリエーション企画'], qualifications=['介護福祉士', '普通自動車免許'], experience_years=5),
        Candidate(name='伊藤 優子', skills=['Word', 'Excel', 'PowerPoint', '電話対応'], qualifications=['簿記3級'], experience_years=1),
        Candidate(name='渡辺 拓也', skills=['Python', 'AWS', 'Docker', 'Go言語'], qualifications=[], experience_years=4)
    ]
    
    db.session.add_all(jobs_to_add)
    db.session.add_all(candidates_to_add)
    db.session.commit()
    print(f"{len(jobs_to_add)}件の多様な求人データを投入しました。")