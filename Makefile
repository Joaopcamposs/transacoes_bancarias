export IMAGE_NAME = joaopcamposs/transacoes_bancarias
export TAG = latest
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
export COMPOSE_NAME=transacoes_bancarias

ruff:
	ruff format . && ruff check . --fix

run:
	fastapi dev contextos_de_negocios/main.py

docker_pull:
	docker pull $(IMAGE_NAME):$(TAG)

docker_stop:
	docker rm -f $(COMPOSE_NAME) || true

docker_clean:
	docker system prune -f

docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) -f $(DOCKERFILE_PATH) .

docker-run:
	docker run --name $(COMPOSE_NAME) -p 8001:8000 -d --restart always $(IMAGE_NAME):$(TAG)

docker-stop:
	docker rm -f $(COMPOSE_NAME)

docker-logs:
	docker logs $(COMPOSE_NAME)

docker-build-up-compose:
	docker-compose -f infra/docker-compose.yml --env-file .env -p $(COMPOSE_NAME) up --build -d

install:
	uv sync

venv:
	uv venv