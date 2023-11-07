# Django Ice Cream Truck App - ict :ice_cream:

## Project Description :page_facing_up:

This is a Django web application for managing an ice cream truck business. It allows customers to purchase ice cream, shaved ice, and snacks, and provides an inventory view for the truck owner. Additionally, it tracks customer spending.

## Project Setup

### Cloning the Repository

1. Clone the repository:

   ```shell
   git clone https://github.com/rajgauravv/ict.git
   cd ict
   
### Creating a virtual environment 
1. Create a virtual environment:
    ```shell
    python3 -m venv env
2. Activate virtual environment
    ```shell
    source env/bin/activate  # On Ubuntu

### Installing requirements
1. Install requirements.txt file
    ```shell
    pip install -r requirements.txt

### Django project setup
1. Use python manage.py migrate
2. Use```python manage.py collectstatic --noinput```
3. Create superuser - python manage.py createsuperuser
4. To load data into database sqlite3, open python manage shell using ```python manage.py shell```and write the following script
```python
from customers.initialize_data import load_customers_data
load_customers_data()
```
6. To create users, open python manage shell using ```python manage.py shell```and write the following script
```python
from ice_cream_truck.initialize_data import *
load_ice_cream_data()
load_shaved_ice_data()
load_snack_bar_data()
```
_**Note: Make 2 users with 1 user being admin and 1 without admin**_

## Running the project :running:

Now run the app using command ```python manage.py runserver```

## Testing :hourglass:

For testing run command ```python manage.py test api.tests```
For testing run command ```python manage.py test ice_cream_truck.tests```

## Docker Setup (Optional)
1. Build the Docker image:
   ```bash
   docker build -t ice-cream-truck-app .
2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 ice-cream-truck-app

## Contributing :handshake:
Feel free to contribute to this project by creating pull requests. Your contributions are greatly appreciated!

Enjoy managing your ice cream truck business with this Django app! :ice_cream: :truck:
