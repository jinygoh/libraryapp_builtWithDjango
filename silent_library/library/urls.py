# This file defines the URL patterns for the library application.
# It is related to the `views.py` file, as it maps URLs to views.

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # The home page.
    path('', views.home, name='home'),
    # The user registration page.
    path('register/', views.register, name='register'),
    # The registration complete page.
    path('register/complete/', views.registration_complete, name='registration_complete'),
    # The user login page.
    path('login/', views.login_view, name='login'),
    # The user logout page.
    path('logout/', views.logout_view, name='logout'),
    # The user dashboard page.
    path('dashboard/', views.dashboard, name='dashboard'),
    # The user profile page.
    path('profile/', views.profile, name='profile'),
    # The book search page.
    path('search/', views.search_books, name='search_books'),
    # The book detail page.
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='library/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='library/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='library/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='library/password_reset_complete.html'), name='password_reset_complete'),

    # Admin URLs
    # The admin dashboard page.
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    # The admin books page.
    path('admin/books/', views.admin_books, name='admin_books'),
    # The add book page.
    path('admin/books/add/', views.add_book, name='add_book'),
    # The edit book page.
    path('admin/books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    # The delete book page.
    path('admin/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    # The send overdue emails page.
    path('admin/send_overdue_emails/', views.bulk_email_overdue_borrowers, name='send_overdue_emails'),
]
