# Base image
FROM python:3.10

# Set working directory
WORKDIR /usr/src/app

# Install dependencies
COPY ./requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the expected port
EXPOSE 8000

# Use the entry point to run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
