# ======================================
# Base image
# ======================================
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# ======================================
# Development image
# ======================================
FROM base AS development

# Expose dev port
EXPOSE 8000

# Default command: Django with autoreload
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ======================================
# Production image
# ======================================
FROM base AS production

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose prod port
EXPOSE 8080

# Use Gunicorn in production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "myproject.wsgi:application"]
