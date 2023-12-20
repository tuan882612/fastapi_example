FROM python:3.12-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y make

COPY Makefile ./
COPY requirements.txt ./
COPY src/ ./src/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 2000

CMD ["make", "start"]
