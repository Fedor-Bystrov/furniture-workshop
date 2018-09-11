FROM python:3.7

EXPOSE 3130
WORKDIR /usr/src/workshop

COPY . .

RUN pip install pipenv
RUN pipenv install
RUN mkdir /logs
CMD pipenv run uwsgi workshop.ini