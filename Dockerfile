# Base image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose the port the app runs on
ENV PORT 8000

# Install dependencies
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean


# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the Django project code into the container
COPY . .

# Change directory to aipetnamer
WORKDIR /app/aipetnamer

# Collect static files
RUN python manage.py collectstatic --noinput

# Start the server
CMD ["sh", "-c", "python manage.py migrate && gunicorn aipetnamer.wsgi:application --bind 0.0.0.0:$PORT"]
