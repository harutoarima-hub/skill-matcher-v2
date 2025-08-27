FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 起動スクリプトをコンテナにコピーします
COPY start.sh .

# 実行権限を付与します (gitで設定済みですが念のため)
RUN chmod +x ./start.sh

EXPOSE 8000

# 起動スクリプトを実行するよう設定します
ENTRYPOINT ["./start.sh"]