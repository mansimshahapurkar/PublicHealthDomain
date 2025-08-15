# ========================
# Base Stage (common deps)
# ========================
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


# ========================
# Development Stage
# ========================
FROM base AS development

# Install extra tools if needed for dev
RUN pip install watchdog  # optional for auto-reload

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# ========================
# Production Stage
# ========================
FROM base AS production

COPY . .

# Collect static files (optional)
RUN python manage.py collectstatic --noinput

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "myproject.wsgi:application"]
