from flask import Blueprint, jsonify, request
from .db import db
from .models import Job
from .match import extract_keywords_with_gemini, calculate_similarity_score

api = Blueprint("api", __name__)

@api.get("/jobs")
def list_jobs():
    return jsonify([j.to_dict() for j in Job.query.all()])

@api.route('/match/ad_hoc', methods=['POST'])
def ad_hoc_match():
    data = request.get_json(force=True)
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # フロントエンドから送られてくるプルダウンと自由記述の両方を受け取る
    location = data.get('location')
    sector = data.get('sector')
    conditions = data.get('conditions', [])
    user_profile_text = data.get('profile_text', '')

    # 最初に、プルダウンの条件で求人を絞り込む
    query = Job.query
    if location:
        query = query.filter(Job.location == location)
    if sector:
        query = query.filter(Job.sector == sector)
    
    # チェックボックスの条件は、キーワードに含まれているかで絞り込む
    if conditions:
        for cond in conditions:
            # Job.keywords は JSON 型なので、特定の文字列を含むかで検索します
            # この書き方はデータベースの種類に依存する場合があります
            query = query.filter(Job.keywords.op('->>')('$').contains(cond))
            
    filtered_jobs = query.all()

    # AIによるキーワード抽出は、自由記述欄が入力されている場合のみ実行
    user_keywords = set()
    if user_profile_text:
        user_keywords = extract_keywords_with_gemini(user_profile_text)
    
    results = []
    for job in filtered_jobs:
        # スコア計算
        score, reasons = calculate_similarity_score(user_keywords, job, conditions)
        
        # 絞り込み条件に合致しているだけでも最低スコアを与える
        if not user_profile_text and (location or sector or conditions):
            score = max(score, 0.1) # 最低10点
            if "選択条件に合致" not in reasons:
                reasons.append("選択条件に合致")

        if score >= 0.1: # スコアが10点以上のものだけ表示
            results.append({
                'job': job.to_dict(), 
                'score': score, 
                'reasons': reasons
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'results': results})