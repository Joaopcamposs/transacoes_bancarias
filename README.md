# Transacoes bancárias

Aplicação desenvolvida com Python, FastAPI, SQLAlchemy, Postgres e Docker. 

Fluxo de build e deploy automático através do docker-hub e github actions.

Há um arquivo Makefile com vários comandos disponíveis.

Requisitos para executar a aplicação:
 - Docker
 - Docker-compose
 - Make (opcional)

Para executar a aplicação, basta executar algum dos comandos abaixo:
 - clone o repositório: `git clone https://github.com/Joaopcamposs/transacoes_bancarias`
 - entre na pasta do projeto: `cd transacoes_bancarias`
 - Baixe o arquivo `.env` e coloque-o na pasta raiz: [link](https://drive.google.com/file/d/18zA9D0HyxaqBqNzbjZHhWDdu8IKRWpSx/view?usp=drive_link)
 - Use um dos comandos: `make docker-compose-run` ou `docker-compose -f infra/docker-compose.yml --env-file .env up -d`

Esse comando iniciará a API e o banco de dados Postgres, dentro de um container compose do Docker.

Após iniciar, a aplicação estará disponível em http://localhost:8001/docs, no qual terá vários endpoints disponíveis 
para testar através da documentação swagger gerada automaticamente pelo FastAPI.

A aplicação também está hospedada na AWS e disponível através do link: http://18.117.123.228:8001/docs

A aplicação também conta com uma implementação do Sentry, para monitorar performance e erros. Porém esse por padrão é privada apenas para membros.

<details>
<summary> usuário padrão inicial da aplicação: </summary>
email: admin@email.com | senha: 123456789
</details>


