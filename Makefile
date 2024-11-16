IMAGE_NAME = joaopcamposs/transacoes_bancarias
TAG = latest

ruff:
	ruff format . && ruff check . --fix

run:
	fastapi dev contextos_de_negocios/main.py

docker_pull:
	docker pull $(IMAGE_NAME):$(TAG)

docker_stop:
	docker rm -f transacoes_bancarias || true

docker_clean:
	docker system prune -f

docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) -f $(DOCKERFILE_PATH) .

docker-run:
	docker run --name transacoes_bancarias -p 8001:8000 -d --restart always $(IMAGE_NAME):$(TAG)

docker-stop:
	docker rm -f transacoes_bancarias

docker-logs:
	docker logs transacoes_bancarias

docker-build-up-compose:
	docker-compose -f infra/docker-compose.yml --env-file .env up --build -d

run-postgres:
	docker-compose -f infra/docker-compose.yml --env-file .env up -d postgres_transacoes_bancarias

docker-compose-run:
	docker-compose -f infra/docker-compose.yml --env-file .env up -d

exportar-dependencias:
	pip freeze > infra/requirements.txt

instalar-dependencias:
	pip install -r infra/requirements.txt