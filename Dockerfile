FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Use Render's default runtime path so build-time and runtime paths match
WORKDIR /opt/render/project/src

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy and make entrypoint executable; run migrations at container start
COPY entrypoint.sh /opt/render/project/src/entrypoint.sh
RUN chmod +x /opt/render/project/src/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/opt/render/project/src/entrypoint.sh"]
