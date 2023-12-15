# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ARG OPENAI_API_KEY
ARG FLASK_RUN_PORT
ENV OPENAI_API_KEY $OPENAI_API_KEY
ENV FLASK_RUN_PORT $FLASK_RUN_PORT


WORKDIR /python-docker


COPY . .

RUN pip3 install -r requirements.txt
CMD [ "gunicorn", "--worker-class", "gevent", "app:app", "--timeout", "120", "--bind", "0.0.0.0:39990"]