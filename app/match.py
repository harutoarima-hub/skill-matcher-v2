# app/match.py

def calculate_holistic_score(candidate_data, job):
    """候補者と求人の総合的なマッチスコアを計算する"""
    
    # 各項目の重み付け
    weights = {
        'skills': 0.5,
        'qualifications': 0.3,
        'experience': 0.2
    }
    
    total_score = 0
    reasons = []

    # 1. スキル・経験のマッチ度 (50%)
    user_skills = set(candidate_data.get('skills', []))
    required_skills = set(job.required_skills or [])
    if required_skills:
        matched_skills = user_skills.intersection(required_skills)
        skill_score = len(matched_skills) / len(required_skills)
        total_score += skill_score * weights['skills']
        if matched_skills:
            reasons.append(f"スキルが一致: {', '.join(matched_skills)}")

    # 2. 資格のマッチ度 (30%)
    user_qualifications = set(candidate_data.get('qualifications', []))
    required_qualifications = set(job.required_qualifications or [])
    if required_qualifications:
        if required_qualifications.issubset(user_qualifications):
            total_score += 1.0 * weights['qualifications']
            reasons.append("必須資格を全て満たしています")
        else:
            # 必須資格がなければスコア0（厳しい判定）
            missing_quals = required_qualifications - user_qualifications
            reasons.append(f"必須資格が不足: {', '.join(missing_quals)}")
            return 0, reasons
            
    # 3. 経験年数のマッチ度 (20%)
    user_exp = candidate_data.get('experience_years', 0)
    required_exp = job.experience_years or 0
    if required_exp > 0:
        if user_exp >= required_exp:
            total_score += 1.0 * weights['experience']
            reasons.append(f"経験年数を満たしています ({user_exp}年)")
        else:
            # 経験年数が足りない場合は、割合に応じてスコアを追加
            exp_score = (user_exp / required_exp) * weights['experience']
            total_score += exp_score
            reasons.append(f"経験年数が不足 (必須:{required_exp}年)")
    else:
        # 経験年数が問われない場合は、経験スコアは満点とする
        total_score += 1.0 * weights['experience']
        reasons.append("経験年数不問")

    # nice_to_have項目があればボーナス加点
    nice_to_haves = set(job.nice_to_have or [])
    matched_nice = user_skills.union(user_qualifications).intersection(nice_to_haves)
    if matched_nice:
        bonus = 0.05 * len(matched_nice) # 1つにつき5%加点
        total_score += bonus
        reasons.append(f"歓迎項目に合致: {', '.join(matched_nice)}")

    return min(round(total_score, 2), 1.0), reasons # スコアが1を超えないように調整