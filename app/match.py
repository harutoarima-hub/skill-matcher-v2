from .models import Job, Candidate

# 代表スキルへ正規化（非ITを広くカバー）
SKILL_MAP = {
    # 営業
    "営業": "営業", "法人営業": "営業(B2B)", "toB営業": "営業(B2B)", "b2b": "営業(B2B)", "個人営業": "営業(B2C)", "toC営業": "営業(B2C)", "b2c": "営業(B2C)", "新規開拓": "新規開拓", "既存深耕": "既存深耕",
    # 接客・小売・CS
    "接客": "接客", "販売": "販売", "小売": "小売", "店長": "店長", "エリアマネージャー": "エリアマネ", "cs": "CS", "カスタマーサポート": "CS", "カスタマーサクセス": "CS",
    # 飲食
    "飲食": "飲食", "ホール": "飲食ホール", "キッチン": "飲食キッチン", "調理": "調理", "衛生管理": "衛生管理",
    # 建設・施工
    "施工管理": "施工管理", "建築": "建築", "土木": "土木", "電気工事": "電気工事", "cad": "CAD",
    # 物流・製造
    "物流": "物流", "倉庫": "物流", "在庫管理": "在庫管理", "配車": "配車", "ドライバー": "ドライバー",
    "製造": "製造", "品質管理": "品質管理", "安全衛生": "安全衛生",
    # 事務・バックオフィス
    "一般事務": "一般事務", "営業事務": "営業事務", "総務": "総務", "人事": "人事", "採用": "採用",
    "経理": "経理", "財務": "財務", "労務": "労務", "庶務": "庶務",
    # マーケ・企画
    "マーケティング": "マーケ", "sns運用": "SNS運用", "広告運用": "広告運用", "広報": "広報", "pr": "広報", "販促": "販促",
    "企画": "企画", "商品企画": "商品企画", "プロダクトマネジメント": "PdM", "プロジェクト管理": "PM",
    # データ・分析
    "データ分析": "データ分析", "tableau": "Tableau", "excel": "Excel", "関数": "Excel",
    # 教育・医療・介護
    "保育": "保育", "教員": "教員", "塾講師": "講師", "介護": "介護", "介護福祉士": "介護", "看護": "看護師", "看護師": "看護師",
    # IT（既存も残す）
    "python": "Python", "flask": "Flask", "sql": "SQL", "docker": "Docker", "aws": "AWS",
    "javascript": "JavaScript", "react": "React", "html": "HTML", "css": "CSS", "fastapi": "FastAPI",
    "kotlin": "Kotlin", "android": "Android", "swift": "Swift", "ios": "iOS"
}

def _norm_skill(s: str) -> str:
    if not s: return ""
    k = s.strip().lower()
    return SKILL_MAP.get(k, s.strip())

def _norm_list(xs):
    return sorted({_norm_skill(x) for x in (xs or []) if (x or "").strip()})

def score(job: Job, c: Candidate):
    must = set(_norm_list(job.must_have_skills))
    nice = set(_norm_list(job.nice_to_have_skills))
    cs   = set(_norm_list(c.skills))

    hard    = (len(must & cs) / len(must)) if must else 1.0
    soft    = (len(nice & cs) / max(1, len(nice)))
    salary  = 1.0 if c.desired_min_salary <= (job.max_salary or 0) else 0.0
    loc     = 1.0 if (c.desired_location or "").lower() == (job.location or "").lower() else 0.0
    total   = round(0.6*hard + 0.2*soft + 0.15*salary + 0.05*loc, 3)

    reasons = []
    reasons.append(f"必須 {len(must & cs)}/{len(must)}")
    reasons.append(f"歓迎 {len(nice & cs)}/{len(nice)}")
    reasons.append("年収OK" if salary else "年収NG")
    reasons.append("勤務地OK" if loc else "勤務地NG")
    return total, ", ".join(reasons)

def rank_for_job(job: Job, candidates):
    items=[]
    for c in candidates:
        s, r = score(job, c)
        items.append({"candidate":{
            "id": c.id, "name": c.name, "skills": _norm_list(c.skills), "years": c.years,
            "desired_location": c.desired_location, "desired_min_salary": c.desired_min_salary,
            "availability": c.availability
        },"score": s,"reasons": r})
    items.sort(key=lambda x: x["score"], reverse=True)
    return items

def calculate_match_score(user_skills, must_haves, nice_to_haves):
    """一人のユーザーと一つの求人のマッチスコアを計算する"""
    score = 0
    reasons = []
    
    user_skills_set = set(user_skills or [])
    must_haves_set = set(must_haves or [])
    nice_to_haves_set = set(nice_to_haves or [])

    # 必須スキルが一つでも欠けていたら、マッチしない (スコア0)
    if not must_haves_set.issubset(user_skills_set):
        missing = must_haves_set - user_skills_set
        reasons.append(f"必須スキル不足: {', '.join(missing)}")
        return 0, reasons

    # 必須スキルは全て満たしている
    if must_haves_set:
        score += 0.5  # ベーススコア
        reasons.append(f"必須スキルを全て満たしています: {', '.join(must_haves_set)}")

    # あれば嬉しいスキル（加点）
    matched_nice_to_haves = user_skills_set.intersection(nice_to_haves_set)
    if matched_nice_to_haves:
        # あれば嬉しいスキルのうち、持っている割合に応じてスコアを加算 (最大0.5点)
        bonus_score = 0.5 * (len(matched_nice_to_haves) / len(nice_to_haves_set))
        score += bonus_score
        reasons.append(f"加点スキル: {', '.join(matched_nice_to_haves)}")
        
    return round(score, 2), reasons
