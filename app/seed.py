from .db import db
from .models import Job

def seed_data():
    """データベースに初期データを投入する関数"""
    
    db.session.query(Job).delete()
    
    # --- 50件の元となる、詳細な求人データ ---
    jobs_data = [
        {
            "title": "カフェ・バリスタ",
            "sector": "飲食",
            "company": "Blue Mountain Cafe",
            "location": "東京",
            "min_salary": 300,
            "max_salary": 400,
            "description": "お客様に最高のコーヒー体験を提供するカフェで、ドリンク作成、接客、レジ業務を担当していただきます。コーヒーへの情熱がある方を歓迎します。",
            "requirements": "・週3日以上勤務可能な方\n・土日祝日に勤務可能な方\n・基本的な接客スキル",
            "welcome_requirements": "・バリスタ経験1年以上\n・英語での日常会話スキル",
            "keywords": ["カフェ", "バリスタ", "接客", "コーヒー", "東京"]
        },
        {
            "title": "ライフスタイル雑貨の販売スタッフ",
            "sector": "販売",
            "company": "Modern Living",
            "location": "大阪",
            "min_salary": 320,
            "max_salary": 450,
            "description": "シンプルで質の高い生活を提案するインテリア・雑貨店での販売、商品管理、ディスプレイ作成などをお任せします。お客様の生活に寄り添う仕事です。",
            "requirements": "・販売・接客経験2年以上\n・在庫管理システムの利用経験",
            "welcome_requirements": "・インテリアコーディネーター資格\n・ギフトラッピングスキル",
            "keywords": ["販売", "雑貨", "インテリア", "接客", "大阪"]
        },
        {
            "title": "介護スタッフ（デイサービス）",
            "sector": "介護",
            "company": "ふれあいデイサービスセンター",
            "location": "福岡",
            "min_salary": 340,
            "max_salary": 480,
            "description": "利用者様の日常生活のサポート（食事、入浴、移動の介助）や、レクリエーションの企画・実行を行います。チームワークを大切にしています。",
            "requirements": "・介護職員初任者研修修了者\n・普通自動車免許（AT限定可）",
            "welcome_requirements": "・介護福祉士資格\n・レクリエーション介護士資格",
            "keywords": ["介護", "デイサービス", "介護福祉士", "初任者研修", "福岡"]
        },
        {
            "title": "人事・採用アシスタント",
            "sector": "事務",
            "company": "グローバル・ビジネス・パートナーズ",
            "location": "リモート",
            "min_salary": 350,
            "max_salary": 500,
            "description": "成長中の企業で、人事・採用活動のアシスタント業務を担当します。候補者との連絡調整、面接設定、データ入力などが主な業務です。",
            "requirements": "・事務経験2年以上\n・Word, Excel, PowerPointの基本操作",
            "welcome_requirements": "・人事または採用関連業務の経験\n・ビジネスレベルの英語力",
            "keywords": ["事務", "人事", "採用", "アシスタント", "リモート"]
        },
        {
            "title": "クラウドインフラエンジニア",
            "sector": "IT",
            "company": "NextGen Cloud Solutions",
            "location": "東京",
            "min_salary": 600,
            "max_salary": 900,
            "description": "AWSやGCPを用いたクラウドインフラの設計、構築、運用をお任せします。IaC(Infrastructure as Code)を活用した自動化を推進しています。",
            "requirements": "・AWSまたはGCPの利用経験2年以上\n・Docker, Kubernetesの基礎知識\n・Linuxサーバーの構築・運用経験",
            "welcome_requirements": "・TerraformまたはCloudFormationの利用経験\n・AWS認定ソリューションアーキテクト",
            "keywords": ["IT", "AWS", "GCP", "Docker", "インフラ", "SRE", "東京"]
        }
    ]
    
    # データをデータベースオブジェクトに変換
    jobs_to_add = [Job(**data) for data in jobs_data]
    
    # まとめてデータベースセッションに追加
    db.session.add_all(jobs_to_add)
    
    # 変更をデータベースにコミット
    db.session.commit()
    print(f"{len(jobs_to_add)}件の詳細な求人データを投入しました。")