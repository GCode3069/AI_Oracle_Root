# =============================================================================
# SCARIFY Production Dockerfile
# =============================================================================
FROM python:3.11-slim as base

ARG PYTHON_VERSION=3.11
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=latest

LABEL maintainer="SCARIFY Team" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

RUN groupadd -r scarify && useradd -r -g scarify scarify

RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    curl \
    wget \
    git \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Development Stage
# =============================================================================
FROM base as development

RUN apt-get update && apt-get install -y \
    vim \
    tmux \
    htop \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements*.txt ./

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

COPY . .

RUN chown -R scarify:scarify /app

USER scarify

EXPOSE 8080 9229

CMD ["python", "-m", "scarify.main", "--dev"]

# =============================================================================
# Production Stage
# =============================================================================
FROM base as production

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=scarify:scarify . .

RUN mkdir -p /app/logs /app/output /app/temp /app/models && \
    chown -R scarify:scarify /app

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

USER scarify

EXPOSE 8080

CMD ["python", "-m", "scarify.main"]

# =============================================================================
