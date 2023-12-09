# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN pip3 install flask
RUN pip3 install python-dotenv
RUN pip3 install openai
# RUN pip3 install gunicorn

COPY . .

CMD [ "python3", "-m", "flask", "run", '-p', '39990']