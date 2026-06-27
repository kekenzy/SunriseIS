BACKEND=backend
FRONTEND=frontend

# .envからPROJECT_NAMEを読み込む
include .env
export

BACKEND_CONTAINER=$(PROJECT_NAME)-backend
FRONTEND_CONTAINER=$(PROJECT_NAME)-frontend
DB_CONTAINER=$(PROJECT_NAME)-db

# ─────────────────────────────────────────
# ローカル開発
# ─────────────────────────────────────────
up:
	docker-compose up --build -d
	@echo "起動完了"
	@echo "  フロントエンド : http://localhost:5173"
	@echo "  バックエンドAPI: http://localhost:8000"
	@echo "  pgAdmin       : http://localhost:5050"

down:
	docker-compose down

restart: down up

logs:
	docker-compose logs -f --tail=200

be-logs:
	docker logs -f $(BACKEND_CONTAINER)

fe-logs:
	docker logs -f $(FRONTEND_CONTAINER)

# ─────────────────────────────────────────
# バックエンド操作
# ─────────────────────────────────────────
be-bash:
	docker exec -it $(BACKEND_CONTAINER) bash

migrate:
	docker exec $(BACKEND_CONTAINER) python manage.py migrate

makemigrations:
	docker exec $(BACKEND_CONTAINER) python manage.py makemigrations

createsuperuser:
	docker exec -it $(BACKEND_CONTAINER) python manage.py createsuperuser

collectstatic:
	docker exec $(BACKEND_CONTAINER) python manage.py collectstatic --noinput

seed:
	@bash scripts/init_data.sh

be-test:
	docker exec $(BACKEND_CONTAINER) python manage.py test

be-lint:
	docker exec $(BACKEND_CONTAINER) flake8 .

audit-be:
	docker exec $(BACKEND_CONTAINER) pip-audit

# ─────────────────────────────────────────
# フロントエンド操作
# ─────────────────────────────────────────
fe-bash:
	docker exec -it $(FRONTEND_CONTAINER) sh

fe-install:
	docker exec $(FRONTEND_CONTAINER) npm install

fe-build:
	docker exec $(FRONTEND_CONTAINER) npm run build

fe-lint:
	docker exec $(FRONTEND_CONTAINER) npm run lint

fe-test:
	docker exec $(FRONTEND_CONTAINER) npm run test

audit-fe:
	docker exec $(FRONTEND_CONTAINER) npm audit

# ─────────────────────────────────────────
# DB 操作
# ─────────────────────────────────────────
db-bash:
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

db-backup:
	@bash scripts/backup_db.sh

db-reset:
	@bash scripts/reset_dev.sh

# ─────────────────────────────────────────
# 本番デプロイ
# ─────────────────────────────────────────
prod-up:
	docker-compose -f docker-compose.prod.yml up --build -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-deploy:
	@bash scripts/deploy.sh

prod-migrate:
	docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f --tail=200

deploy: prod-deploy

# ─────────────────────────────────────────
# ショートカット
# ─────────────────────────────────────────
test: be-test fe-test

lint: be-lint fe-lint

audit: audit-be audit-fe

.PHONY: up down restart logs be-logs fe-logs be-bash migrate makemigrations \
	createsuperuser collectstatic seed be-test be-lint audit-be \
	fe-bash fe-install fe-build fe-lint fe-test audit-fe \
	db-bash db-backup db-reset \
	prod-up prod-down prod-deploy prod-migrate prod-logs deploy \
	test lint audit
