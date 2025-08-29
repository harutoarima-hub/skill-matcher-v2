import os
import json
import google.generativeai as genai

# Renderの環境変数からAPIキーを読み込む
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def extract_keywords_with_gemini(text):
    """Geminiを使って、文章からキーワードをJSON形式で抽出する"""
    if not text:
        return set()
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
        return set(keywords_data.get("keywords", []))
    except Exception as e:
        print(f"Gemini API呼び出し中にエラーが発生しました: {e}")
        return set()

def calculate_ai_match_score(user_profile_text, job):
    """Geminiで抽出したキーワードを使ってマッチ度を計算する"""
    user_keywords = extract_keywords_with_gemini(user_profile_text)
    job_keywords = set(job.keywords or [])
    if not user_keywords or not job_keywords:
        return 0, ["キーワードが見つかりません"]

    intersection = len(user_keywords.intersection(job_keywords))
    union = len(user_keywords.union(job_keywords))
    score = intersection / union if union > 0 else 0

    reasons = []
    if intersection > 0:
        reasons.append(f"共通キーワード: {', '.join(user_keywords.intersection(job_keywords))}")

    return round(score, 2), reasons