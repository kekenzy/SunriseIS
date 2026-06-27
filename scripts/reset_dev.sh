#!/bin/bash
# 開発環境リセット（DB再構築）
set -e

echo ">>> 開発環境をリセットします..."
docker compose down -v
docker compose up -d db
sleep 5
docker compose up -d backend frontend
echo ">>> リセット完了。init_data.sh を実行してデータを投入してください。"
