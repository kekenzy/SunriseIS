#!/bin/bash
# 本番デプロイスクリプト
set -e

echo ">>> 本番デプロイを開始します..."

echo ">>> イメージビルド..."
docker compose -f docker-compose.prod.yml build

echo ">>> サービス再起動..."
docker compose -f docker-compose.prod.yml up -d

echo ">>> マイグレーション..."
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate

echo ">>> 静的ファイル収集..."
docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput

echo ">>> デプロイ完了"
