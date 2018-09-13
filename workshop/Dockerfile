FROM python:3.7-slim-stretch

EXPOSE 3130
WORKDIR /usr/src/workshop

ENV DB_USR workshop
ENV DB_PASS workshop
ENV DB_HOST postgres
ENV DB_NAME workshop
ENV DB_PORT 5432
ENV APP_PORT 3130

COPY . .

RUN apt-get update && apt-get install -y gcc
RUN pip3 install pipenv
RUN pipenv install --three
RUN mkdir /logs
CMD pipenv run uwsgi workshop.ini