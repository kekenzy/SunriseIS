---
name: dev-implement
description: 実装エージェント。設計書をもとにコードを書き、ブランチを切ってコミット・プッシュし、PRを作成する。
---
# Dev Implement

設計書をもとに実際のコードを実装するスキル。

## 入力

`args` または前フェーズから引き継いだ設計書。

## ステップ 1: 実装計画

設計書を読み込み、実装タスクを分解する：
- タスク一覧（順序・依存関係）
- 各タスクの概算工数
- リスクの高い箇所の特定

ユーザーに確認してから実装開始。

## ステップ 2: ブランチ作成

```bash
git checkout -b feature/<タスク名>
```

命名規則：`feature/`, `fix/`, `chore/` のプレフィックスを使う。

## ステップ 3: 実装

以下の原則に従って実装する：

**コード品質**
- 関数・クラスは単一責任
- マジックナンバーは定数化
- エラーハンドリングはシステム境界のみ
- コメントは「なぜ」だけ書く（「何を」は書かない）

**セキュリティ**
- 入力値はシステム境界で検証
- SQLインジェクション・XSS・CSRF を防ぐ
- 秘密情報は環境変数で管理

**実装順序**（推奨）
1. データ層（モデル・マイグレーション）
2. ビジネスロジック層
3. APIレイヤー
4. フロントエンド

## ステップ 3.5: Makefile 配置

グローバルポリシーに従い、プロジェクトルートに `Makefile` を配置する。

```bash
# テンプレートが存在する場合はコピー
cp .claude/data/templates/Makefile ./Makefile
```

- `.env` に `PROJECT_NAME` が定義されていることを確認する
- コンテナ名は `$(PROJECT_NAME)-backend` / `$(PROJECT_NAME)-frontend` / `$(PROJECT_NAME)-db` の命名規則に合わせる
- `docker-compose.yml` のサービス名と一致していることを確認する

## ステップ 4: コミット

各タスク完了ごとにコミットする：
```
feat: <変更の概要>
fix: <バグ修正の概要>
chore: <設定・ツール変更>
```

## ステップ 5: PR作成

全タスク完了後、PRを作成する：
- タイトル：変更内容の要約
- 本文：変更点・テスト手順・スクリーンショット（UIの場合）

## スタイルガイド
- 実装中に設計との齟齬を発見したら即座に報告する
- 「とりあえず動く」より「正しく動く」を優先する
- 1PRは1機能・1修正を原則とする

## 実装時の必須チェック（このプロジェクト固有）

### フロントエンド: package-lock.json をコミットに含める
`npm install` 実行後に生成される `package-lock.json` がないと、
Docker ビルド時の `npm ci` が失敗して起動できない。

- `frontend/package-lock.json` が存在することを確認してからコミットする
- `.gitignore` で除外されていないことを確認する

### バックエンド: 全appのマイグレーションファイルを作成してコミットする
新しい Django app を追加したら必ず `makemigrations` を実行してコミットする。
マイグレーションファイルがない状態で起動すると、テーブルが存在せずエラーになる。

```bash
# コンテナ内で実行
python manage.py makemigrations <app_name>

# または全app一括
python manage.py makemigrations
```

対象app（このプロジェクト）: accounts, notices, dashboard, billing, events
各appの `migrations/0001_initial.py` がコミットに含まれていることを確認する。

### docker-compose.yml: container_name を明示する
`container_name` を省略すると Docker Compose が自動生成する名前（例: `sunriseis-backend-1`）になり、
Makefile の `$(PROJECT_NAME)-backend`（例: `sunrise-is-backend`）と一致せず `make migrate` 等が失敗する。

```yaml
# NG: container_name なし → Docker が自動生成 → Makefile と不一致
services:
  backend:
    build: ./backend

# OK: Makefile の命名規則に合わせて明示
services:
  backend:
    container_name: ${PROJECT_NAME}-backend
    build: ./backend
```

全サービス（frontend / backend / db / pgadmin 等）に必ず設定する。
