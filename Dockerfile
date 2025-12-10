FROM python:3.11-slim

# setar diretorio de trabalho
WORKDIR /transacoes_bancarias

# copiar projeto
COPY . .

# instalar dependencias
RUN apt-get update && apt-get -y install python3-lxml python3-dev && apt-get -y install nginx && apt-get clean

# configurar variáveis de ambiente de linguagem e horario
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

# instalar dependencias do python
RUN pip install --upgrade pip
RUN pip install uv
RUN uv sync && uv venv

# Adiciona o .venv/bin ao PATH do container
ENV PATH="/transacoes_bancarias/.venv/bin:$PATH"
ENV PYTHONPATH=/transacoes_bancarias

# expor a porta
EXPOSE 8000

# executar o app
CMD ["uvicorn", "contextos_de_negocios.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--forwarded-allow-ips", "*", "--proxy-headers",  "--log-config", "uvicorn_logging_config.json"]