# Django Bookstore 

An online bookstore written in Django with a custom user authentication model, shopping cart and more.

## Features

- **User Authentication**
  - Signup, login, and logout functionality.
  - Password reset via email.
- **Payment Gateways**
  - Can switch between the two available gateways. (Zibal, PayV1)
  - Receive a tracking code after returning to website.
- **Shopping Cart**
  - View what items are in your cart. (And the total price)
  - All past orders are stored in the Orders page. (Includes the tracking code, date, ordered products, etc.)
- **Advanced Search Form**
  - Search for any book in the database by entering keywords into the search form.
  - More specific searches can be done by specifying the author, category, etc. (uses querysets and Q objects to find the books)
- **Admin Panel**
  - Manage books, categories, orders and profiles.
  - Custom admin model configuration.
- **Profile Management**
  - Users can access their profiles via the dropdown on the navbar. 
  - Each user is able to edit their own profile.

## Project Structure

```bash
.
├── bookstore_project
│   ├── asgi.py                 # ASGI entry point
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI entry point
├── books
│   ├── admin.py                # Book admin configuration
│   ├── apps.py                 # Book app configuration
│   ├── forms.py                # Book forms
│   ├── models.py               # Book models (Book, Category, Review)
│   ├── signals.py              # Book signals for adding books to categories
│   ├── tests.py                # Book tests
│   └── views.py                # Book views
├── orders
│   ├── admin.py                # Order admin configuration
│   ├── apps.py                 # Order app configuration
│   ├── models.py               # Order models (OrderInfo, OrderedProductsInfo, Cart)
│   ├── tests.py                # Order tests
│   ├── urls.py                 # Order URL configuration
│   └── views.py                # Order views
├── pages
│   ├── admin.py                # Pages admin configuration
│   ├── apps.py                 # Pages app configuration
│   ├── forms.py                # Pages forms (Search form, etc.)
│   ├── models.py               # Pages models
│   ├── templatetags            # Additional template tags
│   ├── tests.py                # Pages tests
│   ├── urls.py                 # Pages URL configuration
│   └── views.py                # Pages views
├── users
│   ├── admin.py                # User admin configuration
│   ├── apps.py                 # Blog app configuration
│   ├── forms.py                # User forms (Profile form, etc.)
│   ├── models.py               # User models (CustomUser, Profile)
│   └── tests.py                # User tests
├── media                       # Media files (user uploads)
├── static                      # Static files (css, images, js)
├── staticfiles                 # Static files created by collectstatic
├── templates                   # Templates
├── db.sqlite3                  # SQLite database file
├── manage.py                   # Django's command-line utility
└── requirements.txt            # Python dependencies
```

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/TinyPuff/bookstore_0.git
   ```

2. Install dependencies:

   ```bash
   python -m venv .env
   .venv\Scripts\Activate
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

5. Access the site at `http://127.0.0.1:8000/`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
