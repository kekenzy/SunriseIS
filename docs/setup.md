# 環境構築手順

## 前提条件

- Docker Desktop 4.x 以上（または Docker Engine + Compose v2）
- Git

## ローカル開発環境

### 1. 環境変数設定

```bash
cp .env.example .env
```

`.env` の以下を必ず変更してください：

```
SECRET_KEY=（ランダムな文字列に変更）
POSTGRES_PASSWORD=（任意のパスワード）
PGADMIN_PASSWORD=（任意のパスワード）
```

### 2. コンテナ起動

```bash
docker compose up -d
```

初回はイメージビルドに数分かかります。

### 3. 初期データ投入

```bash
bash scripts/init_data.sh
```

### 4. 動作確認

- http://localhost:5173 → フロントエンド
- http://localhost:8000/api/ → API
- http://localhost:5050 → pgAdmin（`.env` の PGADMIN_EMAIL / PGADMIN_PASSWORD でログイン）

## コンテナ操作

```bash
# 起動
docker compose up -d

# 停止
docker compose down

# ログ確認
docker compose logs -f backend
docker compose logs -f frontend

# DB リセット（全データ消去）
bash scripts/reset_dev.sh && bash scripts/init_data.sh
```

## マイグレーション

```bash
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
```

## よくあるトラブル

### frontend が起動しない
`node_modules` のキャッシュ問題の可能性。以下を実行：
```bash
docker compose down
docker compose up -d --build frontend
```

### DB 接続エラー
`.env` の `POSTGRES_*` 設定と `docker-compose.yml` の値が一致しているか確認。
