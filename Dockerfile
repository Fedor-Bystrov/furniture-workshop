FROM python:3.7-slim-stretch

EXPOSE 3130
WORKDIR /usr/src/workshop

COPY . .

RUN apt-get update && apt-get install -y gcc
RUN pip3 install pipenv
RUN pipenv install --three
RUN mkdir /logs
CMD pipenv run uwsgi workshop.ini