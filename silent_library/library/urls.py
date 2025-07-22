# This file is the URL configuration for the 'library' app.
# It is responsible for routing incoming HTTP requests to the appropriate view functions within the app.
# This file is included by the main URL configuration in 'silent_library/urls.py'.
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# This list defines the URL patterns for the 'library' app.
# Each pattern maps a URL to a view function.
urlpatterns = [
    # This pattern maps the root URL to the 'home' view.
    path('', views.home, name='home'),
    # This pattern maps the 'register/' URL to the 'register' view.
    path('register/', views.register, name='register'),
    # This pattern maps the 'register/complete/' URL to the 'registration_complete' view.
    path('register/complete/', views.registration_complete, name='registration_complete'),
    # This pattern maps the 'login/' URL to the 'login_view' view.
    path('login/', views.login_view, name='login'),
    # This pattern maps the 'logout/' URL to the 'logout_view' view.
    path('logout/', views.logout_view, name='logout'),
    # This pattern maps the 'dashboard/' URL to the 'dashboard' view.
    path('dashboard/', views.dashboard, name='dashboard'),
    # This pattern maps the 'profile/' URL to the 'profile' view.
    path('profile/', views.profile, name='profile'),
    # This pattern maps the 'search/' URL to the 'search_books' view.
    path('search/', views.search_books, name='search_books'),
    # This pattern maps the 'book/<int:book_id>/' URL to the 'book_detail' view.
    # The '<int:book_id>' part is a path converter that captures an integer from the URL.
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    # These patterns are for password reset functionality.
    # They use the built-in Django views for password reset.
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='library/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='library/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='library/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='library/password_reset_complete.html'), name='password_reset_complete'),

    # These patterns are for staff-only functionality.
    # They are used for managing users, books, and other administrative tasks.
    path('staff/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/users/', views.admin_users, name='admin_users'),
    path('staff/users/block/<int:user_id>/', views.block_user, name='block_user'),
    path('staff/users/unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('staff/books/', views.admin_books, name='admin_books'),
    path('staff/books/add/', views.add_book, name='add_book'),
    path('staff/books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('staff/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('staff/send_overdue_emails/', views.bulk_email_overdue_borrowers, name='send_overdue_emails'),

    # These patterns are for borrowing and returning books.
    path('book/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('loan/<int:loan_id>/return/', views.return_book, name='return_book'),
]
