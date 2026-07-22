FROM mcr.microsoft.com/playwright/python:latest

# Create app directory
WORKDIR /usr/src/app

# Copy project files
COPY pyproject.toml .
COPY frontdesk_watch.py .
COPY .env .env

# Install the package and dependencies
RUN pip install --upgrade pip setuptools wheel \
 && pip install .

# Expose nothing — this is a background watcher
CMD ["python", "frontdesk_watch.py"]
