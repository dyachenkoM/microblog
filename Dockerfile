FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    curl \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

WORKDIR /app
COPY . .

ENV PATH="/root/.local/bin:$PATH"

RUN uv sync

WORKDIR /app/src

CMD uv run alembic upgrade head && \
    uv run uvicorn main:main_app --host ${APP_HOST} --port ${APP_PORT} --reload