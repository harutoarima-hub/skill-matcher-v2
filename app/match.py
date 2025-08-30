import os
import json
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

keyword_cache = {}

def extract_keywords_with_gemini(text):
    """Geminiを使って、文章からキーワードをJSON形式で抽出する"""
    if not text:
        return set()
    if text in keyword_cache:
        print("--- [CACHE HIT] 保存された結果を返します ---")
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
        
        # ▼▼▼ Geminiの生の返答をログに出力する行を追加 ▼▼▼
        print(f"--- Geminiからの生の返答: ---\n{response.text}\n--------------------------")
        
        result_text = response.text.strip().replace("```json", "").replace("```", "")
        keywords_data = json.loads(result_text)
        result_set = set(keywords_data.get("keywords", []))
        keyword_cache[text] = result_set
        return result_set
    except Exception as e:
        print(f"Gemini API呼び出し中、またはJSON解析中にエラーが発生しました: {e}")
        return set()

def calculate_similarity_score(user_keywords, job):
    """【スコア計算担当】キーワードを使ってマッチ度を計算する（API呼び出しなし）"""
    job_keywords = set(job.keywords or [])
    if not user_keywords or not job_keywords:
        return 0, ["キーワードが見つかりません"]

    intersection = user_keywords.intersection(job_keywords)
    union = user_keywords.union(job_keywords)
    score = len(intersection) / len(union) if union else 0
    
    reasons = []
    if intersection:
        reasons.append(f"共通キーワード: {', '.join(intersection)}")
    
    return round(score, 2), reasons