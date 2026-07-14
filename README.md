# Tvoy Orekh — Django E-commerce Store
[![Django Tests](https://github.com/littlebitru/tvoy-orekh/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/littlebitru/tvoy-orekh/actions/workflows/tests.yml)
A Django-based online store with user authentication, product catalogue, shopping cart, order checkout and customer purchase history.

The project demonstrates common e-commerce backend workflows and relational database design using Django ORM.

## Features

- User registration and authentication
- Custom user model with email and phone fields
- Product catalogue
- Product search by name and description
- Individual product pages
- Personal shopping cart for each user
- Add, update and remove cart items
- Order checkout
- Customer order history
- Order status management
- Product and order management through Django Admin
- Automated tests for registration and checkout

## Technology Stack

- Python
- Django
- Django ORM
- SQLite
- HTML
- CSS
- Bootstrap
- Pillow

## Database Models

The application contains the following main models:

- `User` — custom user account
- `Product` — product information, price and image
- `CartItem` — products stored in a user's cart
- `Order` — customer order and its status
- `OrderItem` — products included in an order

## Installation

Clone the repository:

```bash
git clone https://github.com/littlebitru/tvoy-orekh.git
cd tvoy-orekh
```

Create and activate a virtual environment.

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```
Create a local environment file from the example:

### Windows

```powershell
Copy-Item .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

Open `.env` and replace the example secret key:

```env
DJANGO_SECRET_KEY=your-secure-secret-key
DJANGO_DEBUG=True
```

The `.env` file contains local configuration and must not be committed to GitHub.

Apply database migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

Open the application:

```text
http://127.0.0.1:8000/
```

## Administration

Create an administrator account:

```bash
python manage.py createsuperuser
```

Open the Django administration panel:

```text
http://127.0.0.1:8000/admin/
```

The administration panel can be used to manage products, users, orders and order statuses.

## Running Tests

Run the automated tests with:

```bash
python manage.py test
```

## What I Practiced

- Django project and application structure
- Custom user models
- Authentication and form processing
- Django ORM relationships
- Product search with Django queries
- Shopping cart logic
- Atomic order creation
- Django Admin configuration
- Automated testing
- Git and GitHub workflow

## Author

Anton Troshkin  
Python Backend Developer
