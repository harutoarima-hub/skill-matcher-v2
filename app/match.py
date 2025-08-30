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

# ▼▼▼ この calculate_similarity_score 関数を、より賢いロジックに置き換えました ▼▼▼
def calculate_similarity_score(user_keywords, job):
    """【スコア計算担当】キーワードの「部分一致」を考慮してマッチ度を計算する"""
    job_keywords = set(job.keywords or [])
    if not user_keywords or not job_keywords:
        return 0, ["キーワードが見つかりません"]

    intersection_count = 0
    matched_keywords = set()

    # 部分一致をチェック
    for u_kw in user_keywords:
        for j_kw in job_keywords:
            if u_kw in j_kw or j_kw in u_kw:
                intersection_count += 1
                matched_keywords.add(u_kw)
                matched_keywords.add(j_kw)
                break # 一度マッチしたら次のユーザーキーワードへ

    # 全体集合の数を計算（重複を考慮）
    union_count = len(user_keywords.union(job_keywords))
    
    score = intersection_count / union_count if union_count else 0
    
    reasons = []
    if matched_keywords:
        # 表示する共通キーワードを整理
        display_keywords = user_keywords.intersection(job_keywords) # 完全一致したものを優先
        if not display_keywords:
             display_keywords = {kw for kw in user_keywords if any(kw in j_kw for j_kw in job_keywords)} # 部分一致したものを表示
        if display_keywords:
             reasons.append(f"共通キーワード: {', '.join(list(display_keywords)[:3])}")

    return round(score, 2), reasons