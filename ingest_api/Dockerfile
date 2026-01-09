FROM python:3.13-slim

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UWSGI_PROCESSES=1 \
    UWSGI_THREADS=16 \
    UWSGI_HARAKIRI=240 \
    DJANGO_SETTINGS_MODULE=config.settings

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["gunicorn", "app:app", \
     "--bind", "0.0.0.0:8005", \
     "--workers", "4", \
     "--threads", "2"]