FROM python:3.8
# Or any preferred Python version.
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
# RUN pip install --no-cache-dir --upgrade -r fastapi, pydantic, uvicorn, SQLAlchemy, requests, celery, passlib[bcrypt], psycopg2, python-jose
# RUN pip install pydantic, uvicorn, SQLAlchemy, requests, celery, passlib[bcrypt], psycopg2, python-jose, "fastapi[all]"
# RUN RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# COPY ./app /code/app

#CMD ["uvicorn", "app.main:app", "--proxy-headers","--host", "127.0.0.1", "--port", "8000"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
