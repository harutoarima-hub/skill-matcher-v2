#!/bin/sh

# コマンドが失敗したら、すぐにスクリプトを終了する
set -e

# データベースのセットアップを実行
echo "データベースを初期化します..."
flask init-db

# Gunicornサーバーを起動
echo "Gunicornサーバーを起動します..."
exec gunicorn --bind 0.0.0.0:8000 "app:create_app()"