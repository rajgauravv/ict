FROM python:3.8.10-slim
LABEL authors="gauravraj"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y python3-dev build-essential
RUN python -m venv /env
RUN /env/bin/pip install --no-cache-dir --upgrade pip
RUN /env/bin/pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Collect static files and apply migrations
RUN /env/bin/python manage.py collectstatic --no-input
RUN /env/bin/python manage.py migrate

# Expose the application's port
EXPOSE 8000

# Run the application using Gunicorn
CMD ["/env/bin/gunicorn", "--workers=2", "ict.wsgi:application", "--bind", "0.0.0.0:8000"]
