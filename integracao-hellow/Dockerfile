FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

RUN uv sync --frozen --no-dev


FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 10001 appuser

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/pyproject.toml /app/uv.lock /app/alembic.ini /app/
COPY --from=builder /app/main.py /app/
COPY --from=builder /app/migrations /app/migrations
COPY --from=builder /app/models /app/models
COPY --from=builder /app/provider /app/provider
COPY --from=builder /app/routes /app/routes
COPY --from=builder /app/service /app/service
COPY --from=builder /app/exceptions /app/exceptions
COPY --from=builder /app/handlers /app/handlers

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
