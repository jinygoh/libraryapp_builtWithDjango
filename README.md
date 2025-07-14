# Django Crash Course

This crash course provides a basic understanding of Django using this project as an example.

## Project Structure

The project is a simple library management system. The main components are:

- `silent_library/`: The main project directory.
  - `settings.py`: Contains the project settings, such as database configuration, installed apps, and middleware.
  - `urls.py`: The main URL configuration for the project. It includes the URLs for the `library` app.
- `library/`: The `library` app, which contains the core functionality of the project.
  - `models.py`: Defines the database models for the app.
  - `views.py`: Contains the views, which handle user requests and return responses.
  - `urls.py`: The URL configuration for the app.
  - `forms.py`: Contains the forms, which handle user input.
  - `admin.py`: Registers the models with the Django admin interface.
  - `templates/`: Contains the HTML templates for the app.
  - `static/`: Contains the static files for the app, such as CSS and JavaScript files.

## Models

Models are Python classes that represent a table in the database. Each attribute of the class represents a column in the table. In this project, the models are defined in `library/models.py`.

For example, the `Book` model is defined as follows:

```python
class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    isbn = models.CharField(max_length=17, unique=True)
    total_copies = models.PositiveIntegerField(default=1, db_index=True)
    available_copies = models.PositiveIntegerField(default=1, db_index=True)
    authors = models.ManyToManyField(Author, through='BookAuthor')
    genres = models.ManyToManyField('Genre', through='BookGenre')
```

This model defines a `books` table with the following columns: `id`, `title`, `isbn`, `total_copies`, and `available_copies`. The `authors` and `genres` fields are many-to-many relationships with the `Author` and `Genre` models, respectively.

## Views

Views are Python functions that take a web request and return a web response. The response can be the HTML contents of a web page, a redirect, an XML document, or an image. In this project, the views are defined in `library/views.py`.

For example, the `home` view is defined as follows:

```python
def home(request):
    return render(request, 'library/home.html')
```

This view renders the `library/home.html` template and returns it as a response.

## URLs

URLs are used to map a URL to a view. In this project, the URLs are defined in `silent_library/urls.py` and `library/urls.py`.

For example, the URL for the `home` view is defined as follows:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

This URL pattern maps the root URL (`/`) to the `home` view.

## Templates

Templates are used to generate HTML dynamically. In this project, the templates are located in the `library/templates/` directory.

For example, the `home.html` template is as follows:

```html
{% extends 'library/base.html' %}

{% block content %}
  <h1>Welcome to the Silent Library</h1>
  <p>
    This is a simple library management system built with Django.
  </p>
{% endblock %}
```

This template extends the `library/base.html` template and overrides the `content` block with its own content.

## Forms

Forms are used to handle user input. In this project, the forms are defined in `library/forms.py`.

For example, the `UserLoginForm` is defined as follows:

```python
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
```

This form has two fields: `username` and `password`. The `password` field uses the `PasswordInput` widget to hide the password as the user types it.

## Admin

The Django admin is a powerful tool that allows you to manage the data in your database. In this project, the models are registered with the admin in `library/admin.py`.

For example, the `Book` model is registered with the admin as follows:

```python
from django.contrib import admin
from .models import Book

admin.site.register(Book)
```

This makes the `Book` model available in the admin interface, where you can add, edit, and delete books.
