#!/bin/sh
set -e

echo "--- [INFO] start.sh を開始します ---"

echo "--- [STEP 1] データベースを初期化します..."
python init_db.py
echo "--- [STEP 1] データベース初期化 完了 ---"


echo "--- [STEP 2] Gunicornサーバーを起動します..."
exec gunicorn --bind 0.0.0.0:8000 wsgi:app