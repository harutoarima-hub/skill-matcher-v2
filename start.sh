#!/bin/sh
set -e

echo "--- Gunicornサーバーを直接起動します ---"
exec gunicorn --bind 0.0.0.0:8000 wsgi:app