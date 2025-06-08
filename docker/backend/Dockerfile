FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         curl \
         git \
         build-essential \
         cmake \
         libglib2.0-0 \
         python3-dev \
         libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN pip install --upgrade pip

COPY script/pyproject_to_requirements.sh /script/pyproject_to_requirements.sh

COPY backend /app
WORKDIR /app

RUN bash /script/pyproject_to_requirements.sh

RUN pip install torch torchvision

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python3", "source_app/api/main.py"]
