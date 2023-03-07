# Base image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean


# Set the working directory
WORKDIR /app/aipetnamer

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . .


# Collect static files
RUN python manage.py collectstatic --noinput

# Start the server
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
