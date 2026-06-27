# Sunrise IS Parent Portal

インターナショナルスクール向け保護者マイページ＋管理システム（Phase 1 MVP）

## クイックスタート

### 必要環境
- Docker Desktop（または Docker Engine + Docker Compose v2）
- Git

### 手順

```bash
# 1. リポジトリのクローン
git clone https://github.com/gw-pf/claude-nagai.git
cd claude-nagai

# 2. 環境変数ファイルの準備
cp .env.example .env
# .env を編集して SECRET_KEY・DB パスワードを変更する

# 3. コンテナ起動
docker compose up -d

# 4. 初期データ投入（初回のみ）
bash scripts/init_data.sh
```

### アクセス先

| サービス | URL |
|---------|-----|
| フロントエンド | http://localhost:5173 |
| バックエンド API | http://localhost:8000/api/ |
| Django 管理画面 | http://localhost:8000/admin/ |
| pgAdmin | http://localhost:5050 |

### デモログイン

| 役割 | メール | パスワード |
|------|--------|-----------|
| 保護者 | parent@example.com | demo1234 |
| 管理者 | admin@example.com | admin1234 |

## 画面構成（Phase 1）

- `/` — スクール公開サイト（日英切替）
- `/login` — ログイン（保護者 / 管理者タブ）
- `/portal` — 保護者ダッシュボード
- `/portal/notices` — お知らせ一覧
- `/admin` — 管理ダッシュボード
- `/admin/notices` — お知らせ配信履歴
- `/admin/notices/compose` — お知らせ配信

## 技術スタック

| レイヤー | 技術 |
|---------|------|
| フロントエンド | Vue.js 3 + Vite + Tailwind CSS + Pinia + vue-i18n |
| バックエンド | Django 5 + Django REST Framework |
| 認証 | JWT（djangorestframework-simplejwt）|
| DB | PostgreSQL 16 |
| コンテナ | Docker Compose |

## ドキュメント

- [環境構築詳細](docs/setup.md)
- [API仕様](docs/api.md)
- [アーキテクチャ](docs/architecture.md)
