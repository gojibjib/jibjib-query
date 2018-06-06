FROM python:2.7-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app/uploads/ uploads/
COPY app/code/ code/

WORKDIR /app/code

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8081", "wsgi"]