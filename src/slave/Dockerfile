FROM python:3.7-alpine3.10

LABEL Author="Johnny Villegas"
LABEL version="1.0"

RUN mkdir -p /slave
WORKDIR /slave

COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD python3 run.py