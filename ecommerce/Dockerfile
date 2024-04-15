# For more information, please refer to https://aka.ms/vscode-docker-python

# Multi-stage builds
# Define a build stage: Use a base image that includes all necessary build tools & dependencies
FROM python:3.12-slim as builder

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for psycopg2
# The key is to structure the Dockerfile 
# so that layers that change less frequently (such as dependencies) are built before 
# layers that change more frequently (such as your application code).
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Define a run-time stage
FROM python:3.12-slim

# Copy Python packages from builder to the runtime container
# Update Dockerfile to copy the entire /usr/local directory from the builder stage to the final
COPY --from=builder /usr/local /usr/local

# Set the working directory
WORKDIR /app

# Ensure that the application code is copied only once in the runtime stage to avoid redundancy and potential permission issues.
COPY . /app

# # Set the PYTHONPATH so that Python knows where to find the Django project
# ENV PYTHONPATH /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser --uid 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run when starting the container
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommerce.wsgi:application"]
