# syntax=docker/dockerfile:1
FROM python:slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
#COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN python manage.py migrate


CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]