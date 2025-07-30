FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    libmariadb-dev \
    pkg-config \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "SMS.asgi:application"]
