# Dockerfile
FROM python:3.10-slim

# Install dependencies for wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
 && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port (the container will listen on port 8000 if we use Gunicorn)
EXPOSE 8000

# For demonstration, we'll use Gunicorn here:
# gunicorn <module>:<app_instance> --bind=0.0.0.0:8000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
