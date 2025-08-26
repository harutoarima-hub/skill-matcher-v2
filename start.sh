#!/bin/sh

set -e

echo "データベースを初期化します..."
flask init-db

echo "Gunicornサーバーを起動します..."
# ↓↓↓ Gunicornの起動ターゲットを wsgi:app に変更します ↓↓↓
exec gunicorn --bind 0.0.0.0:8000 wsgi:app