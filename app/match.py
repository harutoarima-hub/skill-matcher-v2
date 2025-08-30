import os
import json
# import google.generativeai as genai # AIライブラリを一時的に無効化

# genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

keyword_cache = {}

def extract_keywords_with_gemini(text):
    """【デバッグモード】AI呼び出しをスキップし、ダミーのキーワードを返す"""
    print("--- [DEBUG] AI呼び出しをスキップし、ダミーキーワードを返します ---")
    
    # AIが返すであろうキーワードを、ここで偽装します
    # これにより、API呼び出しの負荷なしに、後の計算ロジックをテストできます
    return {"販売", "接客", "東京"}

    # --- 以下、実際のAI呼び出しコードを全てコメントアウト ---
    # if not text:
    #     return set()
    # if text in keyword_cache:
    #     return keyword_cache[text]
    # try:
    #     prompt = f"""..."""
    #     model = genai.GenerativeModel('gemini-1.5-flash-latest')
    #     response = model.generate_content(prompt)
    #     print(f"--- Geminiからの生の返答: ---\n{response.text}\n--------------------------")
    #     result_text = response.text.strip().replace("```json", "").replace("```", "")
    #     keywords_data = json.loads(result_text)
    #     result_set = set(keywords_data.get("keywords", []))
    #     keyword_cache[text] = result_set
    #     return result_set
    # except Exception as e:
    #     print(f"Gemini API呼び出し中、またはJSON解析中にエラーが発生しました: {e}")
    #     return set()

def calculate_similarity_score(user_keywords, job):
    """【スコア計算担当】キーワードを使ってマッチ度を計算する（変更なし）"""
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