FROM python:3.9-bullseye

RUN pip install Flask flask-cors Flask-WTF chess

COPY . /app
WORKDIR /app

CMD python app.py
