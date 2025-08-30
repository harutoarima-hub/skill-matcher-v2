import os
import json
import google.generativeai as genai

# Gemini APIキーをRenderの環境変数から読み込む
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# 一度解析したテキストの結果を保存しておくための、シンプルなキャッシュ
keyword_cache = {}

def extract_keywords_with_gemini(text):
    """Geminiを使って、文章からキーワードをJSON形式で抽出する"""
    if not text:
        return set()
    if text in keyword_cache:
        print("--- [CACHE HIT] 保存された結果を返します ---")
        return keyword_cache[text]
    try:
        # AIへの指示（プロンプト）を正しい複数行文字列の形式に修正
        prompt = f"""
Analyze the following user profile text. Extract key terms related to skills, qualifications, experiences, and personal traits. Return these terms as a single JSON array under the key "keywords".

Example Input:
3年間、飲食店のホールスタッフとして接客経験を積みました。基本的なPC操作も可能です。お客様とのコミュニケーションが得意で、将来的には店長を目指したいと考えています。

Example Output:
{{"keywords": ["飲食店", "ホールスタッフ", "接客経験", "PC操作", "コミュニケーション", "店長"]}}

User Profile Text:
"{text}"
"""
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        
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