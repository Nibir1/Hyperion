# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Prevent Python from writing pyc files to disc and verify stdout buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (needed for some python packages like psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

# Run the application
# (CMD is overridden by docker-compose, but good fallback)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]