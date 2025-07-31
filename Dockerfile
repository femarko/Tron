FROM python:3.10-alpine AS base
WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache curl && python3 -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY src/ ./src

FROM base AS dev
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY tests /app/tests
COPY pytest.ini /app

FROM base AS prod

FROM dev AS test