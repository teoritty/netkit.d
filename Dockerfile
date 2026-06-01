# syntax=docker/dockerfile:1
FROM python:3.13-slim

# ---- System deps -----------------------------------------------------------
# iputils-ping / traceroute are required by the Ping & Traceroute tools.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        iputils-ping \
        traceroute \
    && rm -rf /var/lib/apt/lists/*

# ---- Python deps -----------------------------------------------------------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- App -------------------------------------------------------------------
COPY main.py composition_root.py ./
COPY src/ ./src/
COPY static/ ./static/
COPY templates/ ./templates/

# Run as a non-root user
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000

# Healthcheck hits the index page
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/').status==200 else 1)"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
