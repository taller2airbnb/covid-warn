# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.6
COPY . /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOST=0.0.0.0

RUN pip install -r requirements.txt
RUN pip install -e .

EXPOSE 5000

ENTRYPOINT /app/start.sh
