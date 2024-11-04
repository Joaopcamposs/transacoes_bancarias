# Nome da imagem e tag do projeto (pode ser configurável)
IMAGE_NAME = joaopcamposs/transacoes_bancarias
TAG = latest

# Caminho para o Dockerfile
DOCKERFILE_PATH = infra/Dockerfile

ruff:
	ruff format . && ruff check . --fix

run:
	fastapi dev contextos_de_negocios/main.py

docker-build:
	docker build -t joaopcamposs/transacoes_bancarias:transacoes_bancarias -f $(DOCKERFILE_PATH) .

docker-run:
	docker run --name transacoes_bancarias -p 8000:8000 -d --restart always joaopcamposs/transacoes_bancarias:transacoes_bancarias

docker-stop:
	docker rm -f transacoes_bancarias

docker-logs:
	docker logs transacoes_bancarias

docker-build-up-compose:
	docker-compose -f infra/docker-compose.yml up --build -d

exportar-dependencias:
	pip freeze > infra/requirements.txt

instalar-dependencias:
	pip install -r infra/requirements.txt