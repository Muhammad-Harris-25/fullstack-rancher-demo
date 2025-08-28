# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app
# - PYTHONPATH=/app lets you use absolute imports: `import models`, `import database`, etc.
# - PYTHONDONTWRITEBYTECODE + PYTHONUNBUFFERED = faster, cleaner containers
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install deps (with retries + longer timeout to avoid flaky network failures)
COPY backend/requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && for i in 1 2 3 4 5; do \
      pip install --no-cache-dir --prefer-binary --default-timeout=120 -r requirements.txt && break || \
      echo "pip install failed (attempt $i/5). Retrying..." && sleep 12; \
    done

# Copy app code
COPY backend/ ./

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
