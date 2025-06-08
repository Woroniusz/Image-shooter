FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         curl \
         git \
         build-essential \
         cmake \
         libglib2.0-0 \
         python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY frontend/shooter /app
WORKDIR /app

RUN uv sync

ENV PYTHONPATH=/app

CMD ["uv", "run", "python",  "manage.py", "runserver", "0.0.0.0:8000"]
