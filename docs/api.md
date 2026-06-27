# API 仕様

ベースURL: `http://localhost:8000`

認証: `Authorization: Bearer <access_token>`

## 認証

| Method | Path | 説明 | 認証 |
|--------|------|------|------|
| POST | `/api/auth/login/` | ログイン（JWT発行）| 不要 |
| POST | `/api/auth/token/refresh/` | トークン更新 | 不要 |
| POST | `/api/auth/logout/` | ログアウト（Blacklist）| 要 |
| GET | `/api/auth/me/` | 自分の情報 | 要 |

### ログイン例

```json
POST /api/auth/login/
{
  "email": "parent@example.com",
  "password": "demo1234"
}
→ { "access": "...", "refresh": "..." }
```

## 保護者 API

| Method | Path | 説明 |
|--------|------|------|
| GET | `/api/parent/dashboard/` | ダッシュボードデータ |
| GET | `/api/parent/notices/` | お知らせ一覧 |
| GET | `/api/parent/notices/{id}/` | お知らせ詳細（既読マーク）|
| GET | `/api/parent/children/` | お子さま一覧 |
| GET | `/api/parent/attendance/?year=&month=` | 月次出席 |
| GET | `/api/parent/events/` | 直近イベント |

## 管理者 API

| Method | Path | 説明 |
|--------|------|------|
| GET | `/api/admin/dashboard/` | 管理ダッシュボード |
| GET | `/api/admin/notices/` | お知らせ一覧 |
| POST | `/api/admin/notices/` | お知らせ作成・配信 |
| PATCH | `/api/admin/notices/{id}/` | お知らせ編集 |
| DELETE | `/api/admin/notices/{id}/` | お知らせ削除 |

管理者APIは `IsAdminUser` パーミッション必須。
