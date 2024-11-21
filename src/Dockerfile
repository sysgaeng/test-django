FROM python:3.9-slim-buster

RUN apt-get update && apt-get install gcc libcurl4-openssl-dev libssl-dev -y && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip
RUN mkdir /src
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ARG CI
ARG APP_ENV
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
RUN if [ $CI ]; then python manage.py cron --settings=config.settings.$APP_ENV; fi
