# ─────────────────────────────────────────────
# AI Shield Scanner — Dockerfile
# Base image: Python 3.11 slim (lightweight)
# ─────────────────────────────────────────────

FROM python:3.11-slim

# ── Set working directory inside the container ──
WORKDIR /app

# ── Install system dependencies ──
# gcc + libpq-dev are required by psycopg2 (PostgreSQL driver)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Copy requirements first (Docker layer cache optimisation) ──
# If requirements.txt hasn't changed, Docker skips re-installing packages
COPY backend/requirements.txt .

# ── Install Python dependencies ──
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Copy the entire backend source code ──
COPY backend/ .

# ── Create a non-root user for security (NFR07) ──
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app
USER appuser

# ── Expose the port FastAPI runs on ──
EXPOSE 8000

# ── Health check — Docker will monitor if the app is alive ──
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ── Start the FastAPI application ──
# --host 0.0.0.0  → accept connections from outside the container
# --port 8000     → match the EXPOSE port above
# --reload        → auto-restart on code changes (remove in production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]