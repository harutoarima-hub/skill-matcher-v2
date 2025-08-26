FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# RUN python app/seed.py の行を削除しました

ENV FLASK_APP=app/__init__.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
EXPOSE 8000

# 開発用サーバーから本番用サーバー(gunicorn)に変更
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]