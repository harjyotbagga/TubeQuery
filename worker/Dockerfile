FROM python:3.8.5-alpine 

WORKDIR /usr/src/app

RUN apk update \
    && apk add gcc python3-dev musl-dev zlib-dev jpeg-dev libffi-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .