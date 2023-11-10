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

# Initialize customer and Ice cream models
RUN /env/bin/python manage.py shell -c "from customers.initialize_data import load_customers_data; load_customers_data()"
RUN /env/bin/python manage.py shell -c "from ice_cream_truck.initialize_data import *; load_ice_cream_data();load_shaved_ice_data();load_snack_bar_data();"
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin123
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
RUN /env/bin/python manage.py createsuperuser --noinput

EXPOSE 8000

# Runing application
CMD ["/env/bin/gunicorn", "--workers=2", "ict.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD ["/env/bin/python", "/app/manage.py","runserver","0.0.0.0:8000"]
