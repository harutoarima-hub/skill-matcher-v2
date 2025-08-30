# app/seed.py

from .db import db
from .models import Job
import random

def seed_data():
    """データベースに初期データを投入する関数"""
    
    db.session.query(Job).delete()
    db.session.commit()

    # --- 50件の多様な求人データを生成するための定義 ---
    
    jobs_definitions = {
        "IT": {
            "titles": ["クラウドエンジニア", "フロントエンドデベロッパー", "データアナリスト"],
            "companies": ["TechCloud Solutions", "Innovate Web Co.", "Data Insights Inc."],
            "locations": ["東京", "リモート"],
            "details": [
                ("AWS/GCPを用いたインフラ設計・構築", "Terraform, Kubernetes", "Python, Go"),
                ("React/Vueを使ったWebフロント開発", "TypeScript, Next.js", "UI/UXデザイン, Figma"),
                ("SQLとBIツールを用いたデータ分析", "Python (Pandas, Matplotlib)", "機械学習, Tableau")
            ]
        },
        "飲食": {
            "titles": ["カフェスタッフ", "レストランホール", "調理師"],
            "companies": ["Organic Cafe", "Seaside Grill", "Kitchen Ichiro"],
            "locations": ["東京", "神奈川", "京都"],
            "details": [
                ("接客、ドリンク作成、レジ業務", "バリスタ経験", "ラテアート"),
                ("お客様のご案内、オーダーテイク、配膳", "ワインの知識", "英語対応"),
                ("食材の仕込み、調理、新メニュー開発", "調理師免許", "ジャンル問わず調理経験5年以上")
            ]
        },
        "販売": {
            "titles": ["アパレル販売スタッフ", "ライフスタイル雑貨販売", "店長候補"],
            "companies": ["Urban Threads", "Modern Living", "Style & Co."],
            "locations": ["東京", "大阪", "福岡"],
            "details": [
                ("接客、販売、在庫管理、ディスプレイ", "VMD経験", "顧客管理"),
                ("インテリア雑貨の接客販売、ラッピング", "ギフト販売経験", "商品ディスプレイ"),
                ("店舗運営全般、スタッフ管理、売上管理", "マネジメント経験3年以上", "販売戦略立案")
            ]
        },
        "介護": {
            "titles": ["介護福祉士（デイサービス）", "ケアマネージャー", "訪問介護員"],
            "companies": ["ケアホーム陽だまり", "スマイル・サポート", "ふれあい介護サービス"],
            "locations": ["埼玉", "北海道", "福岡"],
            "details": [
                ("食事・入浴・移動の介助、レクリエーション", "介護福祉士資格", "普通自動車免許"),
                ("ケアプラン作成、利用者様との面談", "介護支援専門員資格", "実務経験5年以上"),
                ("利用者様のご自宅での身体介助・生活援助", "介護職員初-任者研修", "自転車・バイク移動が可能な方")
            ]
        },
        "事務": {
            "titles": ["一般事務", "経理アシスタント", "人事・採用アシスタント"],
            "companies": ["ABC商事", "Global Partners", "Assist Co."],
            "locations": ["東京", "リモート", "大阪"],
            "details": [
                ("データ入力、電話・来客対応、書類作成", "Word, Excel", "PowerPoint"),
                ("請求書発行、経費精算、仕訳入力", "簿記3級以上", "経理実務経験1年以上"),
                ("面接日程調整、候補者連絡、求人票作成", "採用業務経験", "ビジネスメール")
            ]
        }
    }
    
    jobs_to_add = []
    
    for i in range(50):
        sector = random.choice(list(jobs_definitions.keys()))
        job_info = jobs_definitions[sector]
        
        title = random.choice(job_info["titles"])
        company = random.choice(job_info["companies"])
        location = random.choice(job_info["locations"])
        details = random.choice(job_info["details"])
        
        min_sal = random.randint(28, 65) * 10
        max_sal = min_sal + random.randint(10, 30) * 10
        
        description = f"{company}での{title}のお仕事です。{details[0]}などを担当していただきます。"
        reqs_list = details[1].split(', ')
        welcome_reqs_list = details[2].split(', ')
        
        requirements_str = "\n".join([f"・{req}" for req in reqs_list])
        welcome_requirements_str = "\n".join([f"・{req}" for req in welcome_reqs_list])
        
        keywords = [sector, location, title.split('（')[0]] + reqs_list + welcome_reqs_list
        
        job_data = {
            "title": title, "sector": sector, "company": company, "location": location,
            "min_salary": min_sal, "max_salary": max_sal, "description": description,
            "requirements": requirements_str, "welcome_requirements": welcome_requirements_str,
            "keywords": list(set(keywords))
        }
        jobs_to_add.append(Job(**job_data))

    # ▼▼▼ 不要な行を削除しました ▼▼▼
    # jobs_to_add = [Job(**data) for data in jobs_data]
    
    db.session.add_all(jobs_to_add)
    db.session.commit()
    
    print(f"{len(jobs_to_add)}件の詳細な求人データを投入しました。")