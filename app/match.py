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
        return keyword_cache[text]
    try:
        # ▼▼▼ AIへの指示（プロンプト）を、より明確で簡潔なものに修正しました ▼▼▼
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