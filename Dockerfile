FROM python:3.11-slim

# setar diretorio de trabalho
WORKDIR /transacoes_bancarias

# copiar projeto
COPY . .

# instalar dependencias
RUN apt-get update && apt-get -y install python3-lxml python3-dev && apt-get -y install nginx && apt-get clean

# instalar dependencias adicionais para aws
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8

# configurar variáveis de ambiente de linguagem e horario
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

# atualizar pip
RUN python -m pip install --upgrade pip

# instalar dependencias do python
RUN pip install -r infra/requirements.txt || pip install -r requirements.txt

# expor a porta
EXPOSE 8000

# executar o app
CMD uvicorn --host 0.0.0.0 --port 8000 contextos_de_negocios.main:app --workers 1 --log-level info --forwarded-allow-ips="*" --proxy-headers