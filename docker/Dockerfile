# Stage 1: Build stage
FROM python:3.12-slim AS builder

# Create the app directory 
RUN mkdir /app

# Set the working directory 
WORKDIR /app

# Set environment variables to optimize Python 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies first for caching benefit 
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production 
FROM python:3.12-slim

# Create non-root user 
RUN useradd -m -r appuser && \
    mkdir /app && chown -R appuser /app

# Set the working directory 
WORKDIR /app

# Set environment variables to optimize Python 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy and make the entrypoint executable
# COPY entrypoint.sh /app/entrypoint.sh
# RUN chmod +x /app/entrypoint.sh

# Copy application code 
COPY --chown=appuser:appuser . /app


# Switich to non-root user 
USER appuser

# Expose the application port 
EXPOSE 8000

# Add Docker-native healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl --fail http://localhost:8000/health/ || exit 1

# Change CMD to use entrypoint
# CMD ["/app/entrypoint.sh"]
# RUN python manage.py collectstatic --noinput
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "docker.wsgi:application"]


# Don't collectstatic here because volume will overwrite it; run it at runtime
# CMD sh -c "python manage.py collectstatic --noinput && gunicorn docker.wsgi:application --bind 0.0.0.0:8000"