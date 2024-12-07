# Use Python 3.11 as the base image
FROM python:3.11

# Install PostgreSQL development libraries
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements folder into the container
COPY requirements /app/requirements

# Install dependencies
RUN pip install --no-cache-dir -r requirements/local.txt \
    && pip install --no-cache-dir -r requirements/base.txt \
    && pip install --no-cache-dir -r requirements/production.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variable
ENV CLOUD_TELEPHONY_ACTIVE_PROFILE=dev

# Expose the application port
EXPOSE 8080

# Run Alembic and start the app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
