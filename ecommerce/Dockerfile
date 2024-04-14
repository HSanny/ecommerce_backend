# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Set PYTHONPATH so that Python knows where to find the Django project
ENV PYTHONPATH /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommerce.ecommerce.wsgi:application"]

CMD pwd && ls -la && gunicorn --bind 0.0.0.0:8000 ecommerce.wsgi:application
