FROM python:3.14-alpine

EXPOSE 8123
WORKDIR /app
RUN adduser -D appuser

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --locked --no-install-project --compile-bytecode

COPY templates/ /app/templates
COPY yaas.py /app/main.py

USER appuser
CMD [".venv/bin/uvicorn", "main:app", "--proxy-headers", "--forwarded-allow-ips=*", "--host", "0.0.0.0", "--port", "8123"]
