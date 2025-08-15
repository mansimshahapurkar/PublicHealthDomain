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

# Optional: install extra tools for live reload
RUN pip install watchdog

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# ========================
# Production Stage
# ========================
FROM base AS production

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "myproject.wsgi:application"]
