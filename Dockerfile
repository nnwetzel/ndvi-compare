# === Build Stage ===
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

RUN uv python install 3.11

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# === Runtime Stage ===
FROM debian:bookworm-slim

WORKDIR /app

RUN groupadd -r app && useradd -r -g app -d /app -N app

COPY --from=builder /python /python
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:/python/cpython-3.11.11-linux-x86_64-gnu/bin:$PATH"

USER app

CMD ["/app/.venv/bin/uvicorn", "src.ndvi_compare.main:app", "--host", "0.0.0.0", "--port", "8000"]
