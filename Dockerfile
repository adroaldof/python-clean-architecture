FROM python:3.9.12-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV LANG="en_US.UTF-8"

RUN pip install --upgrade pipenv

RUN groupadd --gid 1001 app
RUN useradd --uid 1001 --gid app --home /app app

WORKDIR /app
COPY Pipfile* /app/

RUN pipenv install

COPY . /app/

ENV FLASK_APP=flask_app.py
ENV PYTHONUNBUFFERED=1
ENV FLASK_DEBUG=1

EXPOSE 80

CMD [ "pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=80" ]
