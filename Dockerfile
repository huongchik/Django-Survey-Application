# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Clone the project repository
RUN apt-get update && \
    apt-get install -y git && \
    git clone https://github.com/huongchik/Django-Survey-Application.git /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make database migrations
RUN python manage.py makemigrations && \
    python manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000

# Define environment variable to run server on all interfaces
ENV DJANGO_SUPERUSER_PASSWORD=adminpass \
    DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_EMAIL=admin@example.com

# Run the command to start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
