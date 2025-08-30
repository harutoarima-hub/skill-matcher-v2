import os
import json
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

keyword_cache = {}

def extract_keywords_with_gemini(text):
    """【API呼び出し担当】Geminiを使って、文章からキーワードを抽出する"""
    if not text:
        return set()
    if text in keyword_cache:
        return keyword_cache[text]
    try:
        prompt = f"""
        以下の文章は、ある人物の自己PRです。
        この内容から、その人物のスキル、資格、経験、特性などを表すキーワードを抽出し、
        {{"keywords": ["スキル1", "スキル2", ...]}} という形式のJSONオブジェクトで返してください。

        文章:
        "{text}"
        """
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        result_text = response.text.strip().replace("```json", "").replace("```", "")
        keywords_data = json.loads(result_text)
        result_set = set(keywords_data.get("keywords", []))
        keyword_cache[text] = result_set
        return result_set
    except Exception as e:
        print(f"Gemini API呼び出し中にエラーが発生しました: {e}")
        return set()

def calculate_similarity_score(user_keywords, job, conditions=[]):
    """キーワードと選択条件を総合的に評価してスコアを計算する"""
    job_keywords = set(job.keywords or [])
    
    # ユーザーキーワードと求人キーワードの類似度 (AIスコア)
    ai_score = 0
    if user_keywords and job_keywords:
        intersection = user_keywords.intersection(job_keywords)
        union = user_keywords.union(job_keywords)
        ai_score = len(intersection) / len(union) if union else 0
    
    # 選択条件の一致度 (条件スコア)
    condition_score = 0
    matched_conditions = set(conditions).intersection(job_keywords)
    if conditions:
        condition_score = len(matched_conditions) / len(conditions)

    # 最終スコア (AIスコアと条件スコアを組み合わせる)
    # 両方ある場合は平均、片方だけならそのスコアをそのまま使う
    if user_keywords and conditions and matched_conditions:
        total_score = (ai_score + condition_score) / 2
    else:
        total_score = ai_score or condition_score

    reasons = []
    if ai_score > 0:
        intersection = user_keywords.intersection(job_keywords)
        reasons.append(f"AI共通キーワード: {', '.join(list(intersection)[:2])}")
    if matched_conditions:
        reasons.append(f"選択条件が一致: {', '.join(matched_conditions)}")
    
    return round(total_score, 2), reasons