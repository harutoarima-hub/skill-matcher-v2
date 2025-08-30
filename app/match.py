import os
import json
import google.generativeai as genai

# Gemini APIを呼び出す部分は無効化（デバッグモード）
# genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

keyword_cache = {}

def extract_keywords_with_gemini(text):
    """【デバッグモード】AI呼び出しをスキップし、ダミーのキーワードを返す"""
    print("--- [DEBUG] AI呼び出しをスキップし、ダミーキーワードを返します ---")
    return {"販売", "接客", "東京"}

def calculate_similarity_score(user_keywords, job, conditions=[]):
    """【スコア計算担当】キーワードと選択条件を総合的に評価してスコアを計算する"""
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