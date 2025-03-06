FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8003

CMD ["gunicorn", "--bind", "0.0.0.0:8003", "studybud.wsgi:application"]