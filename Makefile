export IMAGE_NAME = joaopcamposs/transacoes_bancarias
export TAG = latest
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
export COMPOSE_NAME=transacoes_bancarias
export PYTHONPATH=$(CURDIR)

PYTEST = .venv/bin/pytest

# ── Lint / Format ────────────────────────────────────────────
ruff:
	ruff format . && ruff check . --fix

# ── Run ──────────────────────────────────────────────────────
run:
	fastapi dev business_contexts/main.py

# ── Install ──────────────────────────────────────────────────
install:
	uv sync

venv:
	uv venv

# ── Tests ────────────────────────────────────────────────────
test-db-up:
	docker compose -f infra/docker-compose.test.yml up -d --wait

test-db-down:
	docker compose -f infra/docker-compose.test.yml down -v

test: test-db-up
	$(PYTEST) tests/ -v --tb=short; \
	STATUS=$$?; \
	$(MAKE) test-db-down; \
	exit $$STATUS

test-unit:
	$(PYTEST) tests/unit/ -v --tb=short

test-integration: test-db-up
	$(PYTEST) tests/integration/ -v --tb=short; \
	STATUS=$$?; \
	$(MAKE) test-db-down; \
	exit $$STATUS

# ── Docker (produção) ───────────────────────────────────────
docker_pull:
	docker pull $(IMAGE_NAME):$(TAG)

docker_stop:
	docker rm -f $(COMPOSE_NAME) || true

docker_clean:
	docker system prune -f

docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

docker-run:
	docker run --name $(COMPOSE_NAME) -p 8001:8000 -d --restart always $(IMAGE_NAME):$(TAG)

docker-stop:
	docker rm -f $(COMPOSE_NAME)

docker-logs:
	docker logs $(COMPOSE_NAME)

docker-compose-up:
	docker compose -f infra/docker-compose.yml --env-file .env -p $(COMPOSE_NAME) up --build -d

docker-compose-down:
	docker compose -f infra/docker-compose.yml -p $(COMPOSE_NAME) down