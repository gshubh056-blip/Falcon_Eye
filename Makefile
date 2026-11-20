.PHONY: setup lint typecheck test dev demo down

setup:
	uv sync --frozen

lint:
	uv run ruff check .
	uv run ruff format --check .
	cd apps/dashboard && npm ci && npm run lint

typecheck:
	uv run mypy apps/api-gateway/app scripts
	cd apps/dashboard && npm run typecheck

test:
	uv run pytest

demo:
	uv run uvicorn app.main:app --app-dir apps/api-gateway --host 127.0.0.1 --port 8000

down:
	docker compose -f deploy/docker-compose.yml down
