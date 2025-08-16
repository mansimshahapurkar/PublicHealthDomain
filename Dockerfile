# ========================
# Base Stage (common deps)
# ========================
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install common system dependencies (e.g., AWS CLI)
RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    apt-get remove -y curl unzip && \
    apt-get autoremove -y && \
    apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create logs directory (used by both dev and prod)
RUN mkdir -p /app/logs


# ========================
# Development Stage
# ========================
FROM base AS development

# Optional: install extra tools for development
RUN pip install watchdog

# Copy project files
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]


# ========================
# Production Stage
# ========================
FROM base AS production

# Copy project files
COPY . .

# Collect static files (Django specific)
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
