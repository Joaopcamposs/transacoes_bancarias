# Transacoes bancárias

Aplicação desenvolvida com Python, FastAPI, SQLAlchemy, Postgres e Docker. 

Fluxo de build e deploy automático através do docker-hub e github actions.

Há um arquivo Makefile com vários comandos disponíveis.

Requisitos para executar a aplicação:
 - Docker
 - Docker-compose
 - Make (opcional)

Para executar a aplicação, basta executar algum dos comandos abaixo:
 - `make docker-build-up-compose`
 - `docker-compose -f infra/docker-compose.yml up --build -d`

Esse comando iniciará a API e o banco de dados Postgres, dentro de um container compose do Docker.

Após iniciar, a aplicação estará disponível em http://localhost:8001/docs, no qual terá vários endpoints disponíveis 
para testar através da documentação swagger gerada automaticamente pelo FastAPI.

A aplicação também está hospedada na AWS e disponível através do link: http://18.117.123.228/docs

A aplicação também conta com uma implementação do Sentry, para monitorar performance e erros. Porém esse por padrão é privada apenas para membros.

<details>
<summary> usuário padrão inicial da aplicação: </summary>
email: admin@email.com | senha: 123456789
</details>


