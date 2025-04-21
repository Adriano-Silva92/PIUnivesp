FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=Technik3.settings
ENV DJANGO_ENV=prod

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    libffi-dev \
    libglib2.0-dev \
    libxml2 \
    libxslt1.1 \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "Technik3.wsgi:application"]
