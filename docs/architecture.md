# アーキテクチャ概要

## システム構成

```
[ブラウザ] → [Vue.js 3 / Vite :5173]
                    ↓ REST API / JWT
             [Django + DRF :8000]
                    ↓ ORM
             [PostgreSQL :5432]

[pgAdmin :5050] → [PostgreSQL]
```

## ディレクトリ構成

```
claude-nagai/
├── frontend/          # Vue.js 3 プロジェクト
│   ├── src/
│   │   ├── views/     # ページコンポーネント
│   │   ├── components/# 共通コンポーネント
│   │   ├── stores/    # Pinia ストア
│   │   ├── router/    # Vue Router
│   │   ├── api/       # Axios API クライアント
│   │   └── i18n/      # 多言語ファイル（ja/en）
│   └── Dockerfile
├── backend/           # Django プロジェクト
│   ├── config/        # 設定・URLconf・ミドルウェア
│   ├── apps/
│   │   ├── accounts/  # User / Parent / Child モデル・認証
│   │   ├── notices/   # Notice / NoticeRead
│   │   └── dashboard/ # Attendance / Event + API views
│   ├── fixtures/
│   └── Dockerfile
├── scripts/           # 運用スクリプト
├── docs/              # ドキュメント
├── docker-compose.yml
└── .env.example
```

## 認証フロー

1. クライアントが `/api/auth/login/` にメール・パスワードを POST
2. Django が JWT を発行（Access: 15分 / Refresh: 7日）
3. フロントエンドは Access Token を Authorization ヘッダーで送信
4. 期限切れ時は `/api/auth/token/refresh/` で自動更新
5. ログアウト時は Refresh Token を Blacklist に登録

## フェーズ計画

- **Ph1（現在）**: 認証・ダッシュボード・お知らせ・管理画面基本
- **Ph2**: 支払い・出欠連絡・イベントRSVP・申請書類
- **Ph3**: Google Workspace連携・SSO・プッシュ通知
