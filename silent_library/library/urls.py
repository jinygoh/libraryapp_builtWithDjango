# File: silent_library/library/urls.py
# Purpose: This file defines the URL configurations specific to the 'library' app.
# It maps URL patterns to view functions defined in 'views.py' within this app.
# These URLs are typically included into the project's main URL configuration (project's urls.py).
# Each 'path' function call defines a route, its corresponding view, and an optional name
# that can be used to refer to the URL in templates and other parts of the Django application.

from django.urls import path # Imports the `path` function for defining URL patterns.
from django.contrib.auth import views as auth_views # Imports Django's built-in authentication views (for password reset, etc.).
from . import views # Imports views from the current app's 'views.py' file.

# `urlpatterns` is a list of URL patterns that Django will try to match.
# These patterns are relative to the path where this URLconf is included in the project's urls.py.
# For example, if included with `path('library/', include('library.urls'))`, then `path('', ...)` here
# would correspond to `/library/`. If included with `path('', include('library.urls'))`, it corresponds to `/`.
urlpatterns = [
    # Maps the root URL of this app to the `home` view.
    # `name='home'` allows this URL to be referenced as `{% url 'home' %}` in templates.
    path('', views.home, name='home'),

    # User authentication and registration URLs
    path('register/', views.register, name='register'), # URL for user registration.
    path('register/complete/', views.registration_complete, name='registration_complete'), # URL shown after successful registration.
    path('login/', views.login_view, name='login'), # URL for user login.
    path('logout/', views.logout_view, name='logout'), # URL for user logout.

    # User-specific pages
    path('dashboard/', views.dashboard, name='dashboard'), # User dashboard page.
    path('profile/', views.profile, name='profile'), # User profile page.

    # Book related URLs
    path('search/', views.search_books, name='search_books'), # URL for searching books.
    # URL for viewing a specific book's details.
    # `<int:book_id>` captures an integer from the URL and passes it as `book_id` argument to the `book_detail` view.
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    # Password reset URLs using Django's built-in authentication views.
    # These views handle the logic for password reset requests, email sending, and confirmation.
    # `template_name` specifies the custom HTML template to use for each step.
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='library/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='library/password_reset_done.html'), name='password_reset_done'),
    # `<uidb64>` is a base64 encoded user ID, `<token>` is a password reset token.
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='library/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='library/password_reset_complete.html'), name='password_reset_complete'),

    # Custom Admin URLs for managing library content (distinct from Django's built-in admin).
    # These URLs map to custom views for administrative tasks related to the library.
    path('admin/', views.admin_dashboard, name='admin_dashboard'), # Custom admin dashboard.
    path('admin/books/', views.admin_books, name='admin_books'), # Page to list/manage books in custom admin.
    path('admin/books/add/', views.add_book, name='add_book'), # Page to add a new book.
    path('admin/books/edit/<int:book_id>/', views.edit_book, name='edit_book'), # Page to edit an existing book.
    path('admin/books/delete/<int:book_id>/', views.delete_book, name='delete_book'), # Action to delete a book.
]