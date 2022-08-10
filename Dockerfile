FROM python:3.8

COPY requirements.txt /requirements.txt
EXPOSE 8000
RUN pip install -r requirements.txt
COPY ./app /app
WORKDIR /
