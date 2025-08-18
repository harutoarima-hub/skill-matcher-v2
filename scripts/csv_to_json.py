import csv
import json
import sys

# 引数からファイルパスを受け取る
csv_file = sys.argv[1]
json_file = sys.argv[2]

out = []  # ★ここでリストを初期化

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        out.append({
            "title": row.get("求人タイトル", ""),
            "company": row.get("企業名", ""),
            "location": row.get("勤務地", ""),
            "salary": row.get("給与", ""),
            "description": row.get("仕事内容", ""),
        })

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"✅ JSONファイルを出力しました: {json_file}")
