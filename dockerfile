############################
# Stage 1 — Builder
############################
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


############################
# Stage 2 — Runtime
############################
FROM python:3.11-slim

WORKDIR /app

ENV TZ=UTC

# Install cron and tzdata
RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
 && rm -rf /var/lib/apt/lists/*

# Copy installed packages
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Ensure cron and data folders exist
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Copy cron job file
COPY crontab.txt /etc/cron.d/2fa-cron

# Give proper permissions
RUN chmod 0644 /etc/cron.d/2fa-cron

# Ensure cron reads the file
RUN crontab /etc/cron.d/2fa-cron


# Expose port
EXPOSE 8080

# Start cron + uvicorn together
CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8080
