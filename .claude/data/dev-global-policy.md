# 開発グローバルポリシー

このファイルは `dev-manager` / `dev-requirements` / `dev-design` / `dev-implement` / `dev-deploy` スキルが参照します。
プロジェクト固有の上書き指示がない限り、以下の方針を**全フェーズで厳守**してください。

---

## 技術スタック（固定）

| レイヤー | 技術 |
|---------|------|
| フロントエンド | Vue.js 3（Composition API） |
| バックエンド | Django（最新安定版） + Django REST Framework |
| DB | PostgreSQL |
| コンテナ | Docker / Docker Compose |
| DBツール | pgAdmin（Docker に含める） |

---

## Docker 構成方針

- `docker-compose.yml` で以下のサービスを定義する：
  - `frontend` — Vue.js（開発時は `vite`、本番は nginx）
  - `backend` — Django（Gunicorn）
  - `db` — PostgreSQL
  - `pgadmin` — pgAdmin4（DBアクセス確認用）
- 環境変数は `.env` で管理し、`.env.example` をリポジトリに含める
- `.env` は `.gitignore` に追加する

---

## 開発フェーズ方針

- **最初は MVP**（最小限の動作するプロダクト）を優先する
- Want 要件は MVP 後の次フェーズに回す

---

## UI / レスポンシブ

- すべての画面でレスポンシブデザインを考慮する
- ブレークポイント：モバイル（〜767px）/ タブレット（768〜1023px）/ デスクトップ（1024px〜）
- CSS フレームワークはプロジェクトに応じて選定（Tailwind CSS を推奨）

---

## 認証

- **Django 標準認証**（`django.contrib.auth`）を使用する
- JWT を使う場合は `djangorestframework-simplejwt` を採用
- ソーシャルログインが必要な場合は `django-allauth` を採用
- セッション管理・CSRF 対策は Django 標準機能を活用する

---

## セキュリティ（脆弱性対応）

### Django 設定
- `DEBUG = False`（本番環境）
- `SECRET_KEY` は環境変数から取得
- `ALLOWED_HOSTS` を明示的に設定
- `SECURE_HSTS_SECONDS` / `SECURE_SSL_REDIRECT` / `SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE` を本番で有効化

### コーディング
- SQL は ORM を使用し、生 SQL は避ける（必要な場合はパラメータバインド）
- ファイルアップロードは拡張子・サイズを検証し、`MEDIA_ROOT` 外に保存しない
- パスワードは Django の `make_password` / `check_password` を使用
- API には認証・認可チェックを必ず実装（`IsAuthenticated` 等）
- CORS は `django-cors-headers` で制御し、`CORS_ALLOWED_ORIGINS` を明示する
- 依存パッケージは定期的に `pip audit` / `npm audit` でチェック

### レスポンスヘッダー
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Content-Security-Policy` を設定する

---

## ディレクトリ構成（標準）

```
project-root/
├── frontend/          # Vue.js プロジェクト
├── backend/           # Django プロジェクト
├── scripts/           # 初期データ構築・デプロイ・DB マイグレーション等のスクリプト
│   ├── init_data.sh   # 初期データ投入
│   ├── deploy.sh      # デプロイスクリプト
│   └── backup_db.sh   # DB バックアップ
├── docs/              # ドキュメント（MD ファイル）
│   ├── setup.md       # 環境構築手順
│   ├── architecture.md# アーキテクチャ概要
│   └── api.md         # API 仕様
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
└── README.md
```

---

## ドキュメント方針

- 環境構築・デプロイ・運用手順は随時 `docs/` 配下の MD ファイルにまとめる
- スクリプト類は `scripts/` に格納し、ファイル先頭にコメントで用途を記載する
- API 仕様は `docs/api.md` に OpenAPI 形式またはテーブル形式で記載する
- README.md には「クイックスタート」を必ず含める

---

## Makefile（標準）

すべてのプロジェクトルートに `Makefile` を配置する。
テンプレートは `.claude/data/templates/Makefile` を使用し、`PROJECT_NAME` は `.env` から読み込む。

主要ターゲット：

| コマンド | 内容 |
|---------|------|
| `make up` | Docker Compose 起動（--build） |
| `make down` | 停止 |
| `make restart` | 再起動 |
| `make logs` | 全サービスログ |
| `make migrate` | マイグレーション実行 |
| `make seed` | 初期データ投入 |
| `make be-test` | バックエンドテスト |
| `make fe-build` | フロントエンドビルド |
| `make db-reset` | 開発DB リセット |
| `make prod-deploy` | 本番デプロイ |
| `make test` | be-test + fe-test |
| `make lint` | be-lint + fe-lint |
| `make audit` | pip-audit + npm audit |

---

## scripts/ 標準ファイル

| ファイル | 用途 |
|---------|------|
| `scripts/init_data.sh` | 初期データ（フィクスチャ）投入 |
| `scripts/deploy.sh` | 本番デプロイ手順 |
| `scripts/backup_db.sh` | DB バックアップ |
| `scripts/reset_dev.sh` | 開発環境リセット（DB 再構築） |
