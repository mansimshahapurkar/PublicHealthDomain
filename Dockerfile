# ======================================
# Base image
# ======================================
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# ======================================
# Development image
# ======================================
FROM base AS development

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ======================================
# Production image
# ======================================
FROM base AS production

RUN python manage.py collectstatic --noinput
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "myproject.wsgi:application"]
