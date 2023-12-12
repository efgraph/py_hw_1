FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get --yes upgrade

COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x /app/docker-entrypoint.sh
RUN chmod +x /app/wait-for-it.sh

ENTRYPOINT sh /app/docker-entrypoint.sh

EXPOSE 8501