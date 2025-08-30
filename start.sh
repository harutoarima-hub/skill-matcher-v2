#!/bin/sh
set -e

echo "--- Gunicornサーバーを起動します (Timeout: 120s) ---"
exec gunicorn --bind 0.0.0.0:8000 --timeout 120 wsgi:app