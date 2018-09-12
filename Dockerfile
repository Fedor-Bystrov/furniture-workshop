FROM ubuntu:18.10

EXPOSE 3130
WORKDIR /usr/src/workshop
ENV LANG=C.UTF-8

COPY . .

RUN apt-get update && apt-get install -y python3 python3-dev python3-pip
RUN pip3 install pipenv
RUN pipenv install --three
RUN mkdir /logs
CMD pipenv run uwsgi workshop.ini