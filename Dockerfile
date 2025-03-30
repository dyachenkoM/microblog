FROM python:3.7-slim AS backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app
COPY . .

FROM nginx:latest AS frontend

COPY /src/dist/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf

FROM python:3.7-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY --from=backend /app /app
COPY --from=backend /root/.local/bin/uv /usr/local/bin/uv
WORKDIR /app

COPY --from=frontend /usr/share/nginx/html /usr/share/nginx/html
COPY --from=frontend /etc/nginx/nginx.conf /etc/nginx/nginx.conf

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]