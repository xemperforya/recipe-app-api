FROM python:3.9-alpine3.14
LABEL org.opencontainers.image.authors="shantanu"
# run python in unbuffered mode
ENV PYTHONUNBUFFERED = 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user