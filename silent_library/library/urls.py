from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/complete/', views.registration_complete, name='registration_complete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_books, name='search_books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='library/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='library/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='library/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='library/password_reset_complete.html'), name='password_reset_complete'),

    # Staff URLs
    path('staff/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/books/', views.admin_books, name='admin_books'),
    path('staff/books/add/', views.add_book, name='add_book'),
    path('staff/books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('staff/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('staff/send_overdue_emails/', views.bulk_email_overdue_borrowers, name='send_overdue_emails'),
    path('book/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('loan/<int:loan_id>/return/', views.return_book, name='return_book'),
]
