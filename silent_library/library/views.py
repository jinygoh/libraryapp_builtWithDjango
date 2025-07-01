# File: silent_library/library/views.py
# Purpose: This file contains the view functions for the 'library' app.
# Views are Python functions (or classes) that take a web request and return a web response.
# They encapsulate the logic required to process a user's request, interact with models (database),
# process forms, and then render a template (HTML page) or redirect to another URL.
# This file handles user authentication, book display, searching, user profiles, and admin functionalities.

# Django shortcuts provide convenient functions for common tasks.
from django.shortcuts import render, redirect, get_object_or_404
    # render: Combines a given template with a given context dictionary and returns an HttpResponse object with that rendered text.
    # redirect: Returns an HttpResponseRedirect to the appropriate URL for the arguments passed.
    # get_object_or_404: Calls get() on a given model manager, but it raises Http404 instead of the model’s DoesNotExist exception.

# Django's authentication system components.
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
    # login: Logs a user in.
    # logout: Logs a user out.
    # authenticate: Attempts to authenticate a user.
    # update_session_auth_hash: Updates the session hash after a password change to keep the user logged in.

# Decorators for restricting access to views.
from django.contrib.auth.decorators import login_required, user_passes_test
    # login_required: Redirects to the login page if the user is not authenticated.
    # user_passes_test: Checks if a user passes a given test (a callable that takes a User object).

# Utility for reversing URL names to actual paths.
from django.urls import reverse_lazy

# Django's messaging framework for displaying one-time notifications to users.
from django.contrib import messages

# Function for sending emails.
from django.core.mail import send_mail

# Importing models from the current app's models.py.
from .models import Book, Author, Genre, Loan, Review # Removed Genre as it's not directly used in views here, but good to keep if planned.

# Importing forms from the current app's forms.py.
# Note: The import from .forms was duplicated later in the original file; consolidated here.
from .forms import (
    UserRegistrationForm, UserLoginForm, UserEditForm,
    UserEditUsernameEmailForm, UserEditPasswordForm,
    BookForm, ReviewForm
)

# Q objects are used for building complex database queries (e.g., with OR conditions).
from django.db.models import Q

# For accessing project settings (e.g., email configuration).
from django.conf import settings


# Helper function to check if a user is an admin (staff member).
# This is used with the `user_passes_test` decorator for admin-only views.
def is_admin(user):
    """Checks if the given user has staff privileges (is_staff=True)."""
    return user.is_staff # `is_staff` is a boolean field on Django's User model.

# View for the home page.
def home(request):
    """
    Renders the home page of the library.
    Args:
        request: The HttpRequest object.
    Returns:
        HttpResponse: Renders the 'library/home.html' template.
    """
    # `render` takes the request, template name, and optional context dictionary.
    return render(request, 'library/home.html')

# View for user registration.
def register(request):
    """
    Handles user registration.
    If request method is POST, it processes the registration form.
    If the form is valid, it saves the new user, sends a confirmation email,
    displays a success message, and redirects to the registration completion page.
    If request method is GET, it displays an empty registration form.
    Args:
        request: The HttpRequest object.
    Returns:
        HttpResponse: Renders the 'library/register.html' template with the form.
    """
    if request.method == 'POST': # Checks if the form was submitted.
        # Creates a UserRegistrationForm instance populated with data from the request.
        form = UserRegistrationForm(request.POST)
        if form.is_valid(): # Validates the form data.
            user = form.save() # Saves the new user to the database.

            # Prepare and send a confirmation email.
            email_subject = 'Successful Registration on Silent Library'
            email_message = (
                f"Dear {user.first_name},\n\n"
                f"Thank you for registering on our platform. We are excited to have you as a member.\n\n"
                f"Thank you.\nSilent Library Team"
            )
            email_recipient = [user.email] # The user's email address.
            
            try:
                # Sends the email using settings from settings.py.
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=f"Silent Library <{settings.DEFAULT_FROM_EMAIL}>", # Sender's email.
                    recipient_list=email_recipient, # List of recipients.
                    # fail_silently=False # Set to True to not raise an exception on error (not recommended for important emails).
                )
            except Exception as e:
                # If email sending fails, add an error message to be displayed to the user.
                messages.error(request, f'Error sending confirmation email to {email_recipient}: {str(e)}')

            # Display a success message.
            messages.success(request, 'Registration successful. Please check your email for confirmation.')

            # Optional: Automatically log in the user after registration.
            # login(request, user) # This line is commented out; typically, email confirmation is preferred first.

            # Redirects to the 'registration_complete' URL name.
            return redirect('registration_complete')
    else: # If request.method is GET.
        form = UserRegistrationForm() # Creates an empty form instance.
    # Renders the registration template with the form (either empty or with errors).
    return render(request, 'library/register.html', {'form': form})

# View for the registration completion page.
def registration_complete(request):
    """
    Renders a page confirming successful registration.
    Args:
        request: The HttpRequest object.
    Returns:
        HttpResponse: Renders the 'library/registration_complete.html' template.
    """
    return render(request, 'library/registration_complete.html')

# View for user login.
def login_view(request):
    """
    Handles user login.
    If request method is POST, it processes the login form.
    If credentials are valid, it logs the user in and redirects them to their
    dashboard (admin dashboard for staff, regular dashboard for others).
    If request method is GET, it displays an empty login form.
    Args:
        request: The HttpRequest object.
    Returns:,
        HttpResponse: Renders the 'library/login.html' template with the form.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST) # Creates UserLoginForm instance with submitted data.
        if form.is_valid(): # Validates the form.
            username = form.cleaned_data.get('username') # Gets cleaned username.
            password = form.cleaned_data.get('password') # Gets cleaned password.
            user = authenticate(username=username, password=password) # Authenticates the user.
            if user is not None: # If authentication is successful.
                login(request, user) # Logs the user in, creating a session.
                if user.is_staff: # Checks if the user is an admin/staff member.
                    return redirect('admin_dashboard') # Redirects staff to admin dashboard.
                return redirect('dashboard') # Redirects regular users to their dashboard.
            else:
                # If authentication fails, add an error message. (This could be more explicit)
                messages.error(request, 'Invalid username or password.')
    else: # If request.method is GET.
        form = UserLoginForm() # Creates an empty login form.
    return render(request, 'library/login.html', {'form': form})

# View for user logout.
# Requires the user to be logged in.
@login_required # Decorator ensures only logged-in users can access this view.
def logout_view(request):
    """
    Logs the current user out and redirects to the home page.
    Args:
        request: The HttpRequest object.
    Returns:
        HttpResponseRedirect: Redirects to the 'home' URL.
    """
    logout(request) # Logs the user out, clearing their session.
    messages.info(request, "You have been successfully logged out.") # Optional: inform user
    return redirect('home') # Redirects to the home page.

# View for the user's dashboard.
# Requires the user to be logged in.
@login_required
def dashboard(request):
    """
    Displays the user's dashboard, showing their current loans.
    Args:
        request: The HttpRequest object.
    Returns:
        HttpResponse: Renders the 'library/dashboard.html' template with the user's loans.
    """
    # Filters Loan objects to get only those belonging to the currently logged-in user.
    loans = Loan.objects.filter(user=request.user)
    # Renders the dashboard template, passing the loans data in the context.
    return render(request, 'library/dashboard.html', {'loans': loans})


# View for managing user profile (editing details, username/email, password).
# Requires the user to be logged in.
@login_required
def profile(request):
    """
    Handles user profile updates. Supports updating:
    1. Basic profile information (first name, last name) - 'edit_profile' form.
    2. Username and email - 'edit_username_email' form, requires current password.
    3. Password - 'change_password' form, requires current password.
    Args:
        request: The HttpRequest object.
    Returns:
        HttpResponse: Renders the 'library/profile.html' template with relevant forms.
    """
    # Initialize forms for GET request or if a specific form wasn't submitted.
    edit_profile_form = UserEditForm(instance=request.user)
    edit_username_email_form = UserEditUsernameEmailForm(instance=request.user, user=request.user)
    password_form = UserEditPasswordForm(user=request.user)

    if request.method == 'POST':
        # Check which form was submitted based on button name/hidden input.
        if 'edit_profile' in request.POST:
            edit_profile_form = UserEditForm(request.POST, instance=request.user)
            if edit_profile_form.is_valid():
                edit_profile_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile') # Redirect to refresh and show updated info.

        elif 'edit_username_email' in request.POST:
            edit_username_email_form = UserEditUsernameEmailForm(request.POST, instance=request.user, user=request.user)
            if edit_username_email_form.is_valid():
                edit_username_email_form.save()
                messages.success(request, 'Username and email updated successfully.')
                return redirect('profile')

        elif 'change_password' in request.POST:
            password_form = UserEditPasswordForm(request.POST, user=request.user) # Pass request.POST, not request.user for data
            if password_form.is_valid():
                user = password_form.save() # The form's save method handles setting the new password.
                update_session_auth_hash(request, user)  # Important to keep the user logged in!
                messages.success(request, 'Password updated successfully.')
                return redirect('profile')
            # No 'else' here to add form errors to messages; form itself will display errors.

    # Context dictionary to pass forms to the template.
    context = {
        'form': edit_profile_form, # Renamed for clarity in template if using {{ form }}
        'username_email_form': edit_username_email_form,
        'password_form': password_form
    }
    return render(request, 'library/profile.html', context)

# View for searching books.
def search_books(request):
    """
    Searches for books based on a query parameter 'q'.
    The search looks for the query in book titles, author names, and genres.
    Args:
        request: The HttpRequest object. 'q' GET parameter is used for the query.
    Returns:
        HttpResponse: Renders the 'library/search.html' template with search results.
    """
    query = request.GET.get('q') # Retrieves the search query from GET parameters.
    books = Book.objects.all() # Starts with all books.

    if query: # If a query is provided.
        # Filters books using Q objects for OR conditions.
        # __icontains performs a case-insensitive "contains" lookup.
        # .distinct() ensures that if a book matches multiple criteria (e.g., title and author), it only appears once.
        books = books.filter(
            Q(title__icontains=query) |
            Q(authors__first_name__icontains=query) |
            Q(authors__last_name__icontains=query) |
            Q(genres__genre__icontains=query)
        ).distinct()
    # Renders the search results template.
    return render(request, 'library/search.html', {'books': books, 'query': query})

# View for displaying details of a specific book and handling review submissions.
def book_detail(request, book_id):
    """
    Displays details for a specific book, its reviews, and a form to add a new review.
    If the request is POST and the user is authenticated, it processes the review submission.
    Args:
        request: The HttpRequest object.
        book_id: The ID of the book to display, captured from the URL.
    Returns:
        HttpResponse: Renders the 'library/book_detail.html' template.
    """
    # Retrieves the Book object with the given pk (book_id), or raises Http404 if not found.
    book = get_object_or_404(Book, pk=book_id)
    # Retrieves all Review objects associated with this book.
    reviews = Review.objects.filter(book=book)

    review_form = ReviewForm() # Initialize form for GET request

    if request.method == 'POST':
        if not request.user.is_authenticated: # Ensure user is logged in to post a review
            messages.error(request, "You must be logged in to post a review.")
            return redirect('login') # Or redirect to the book detail page itself with a message

        review_form = ReviewForm(request.POST) # Populate form with submitted data.
        if review_form.is_valid():
            review = review_form.save(commit=False) # Create Review object but don't save to DB yet.
            review.book = book # Associate the review with the current book.
            review.user = request.user # Associate the review with the current logged-in user.
            review.save() # Save the review to the database.
            messages.success(request, "Your review has been submitted.")
            # Redirect back to the same book detail page to show the new review and clear the form.
            return redirect('book_detail', book_id=book.pk)
        # If form is not valid, it will be re-rendered with errors below.

    context = {
        'book': book,
        'reviews': reviews,
        'form': review_form # Pass the form (either empty or with errors) to the template.
    }
    return render(request, 'library/book_detail.html', context)

# Custom Admin Views
# These views are protected by the `user_passes_test` decorator, ensuring only admin users (is_staff=True) can access them.
# `login_url=reverse_lazy('admin_login')` (or 'login' if no separate admin login) specifies where to redirect if the test fails.
# Note: The original code used 'admin_login' which might be a custom admin login URL. If using Django's default,
# it would typically redirect to the standard login page or as defined by LOGIN_URL in settings.

@user_passes_test(is_admin, login_url=reverse_lazy('login')) # Assuming 'login' is the general login page.
def admin_dashboard(request):
    """
    Renders the custom admin dashboard page.
    Accessible only by staff users.
    Args:
        request: The HttpRequest object.
    Returns:
        HttpResponse: Renders 'library/admin_dashboard.html'.
    """
    return render(request, 'library/admin_dashboard.html')

@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def admin_books(request):
    """
    Lists all books for the custom admin interface.
    Accessible only by staff users.
    Args:
        request: The HttpRequest object.
    Returns:
        HttpResponse: Renders 'library/admin_books.html' with a list of all books.
    """
    books = Book.objects.all() # Retrieves all Book objects.
    return render(request, 'library/admin_books.html', {'books': books})

@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def add_book(request):
    """
    Handles adding a new book via the custom admin interface.
    If request is POST and form is valid, saves the new book and redirects to admin_books list.
    If request is GET, displays an empty BookForm.
    Accessible only by staff users.
    Args:
        request: The HttpRequest object.
    Returns:
        HttpResponse: Renders 'library/book_form.html' with the BookForm.
    """
    if request.method == 'POST':
        form = BookForm(request.POST) # BookForm with submitted data.
        if form.is_valid():
            form.save() # Saves the new book.
            messages.success(request, f"Book '{form.cleaned_data.get('title')}' added successfully.")
            return redirect('admin_books') # Redirects to the list of books.
    else:
        form = BookForm() # Empty BookForm for GET request.
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Add'}) # Added action for template

@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def edit_book(request, book_id):
    """
    Handles editing an existing book via the custom admin interface.
    If request is POST and form is valid, saves changes and redirects to admin_books list.
    If request is GET, displays BookForm populated with the existing book's data.
    Accessible only by staff users.
    Args:
        request: The HttpRequest object.
        book_id: The ID of the book to edit.
    Returns:
        HttpResponse: Renders 'library/book_form.html' with the BookForm.
    """
    book = get_object_or_404(Book, pk=book_id) # Gets the book to edit or 404.
    if request.method == 'POST':
        # BookForm with submitted data and instance of the book to edit.
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save() # Saves changes to the book.
            messages.success(request, f"Book '{book.title}' updated successfully.")
            return redirect('admin_books') # Redirects to the list of books.
    else:
        # BookForm populated with the existing book's data for GET request.
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Edit', 'book': book}) # Added action and book for template

@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def delete_book(request, book_id):
    """
    Handles deleting a book via the custom admin interface.
    If request is POST, deletes the book and redirects to admin_books list.
    If request is GET, displays a confirmation page.
    Accessible only by staff users.
    Args:
        request: The HttpRequest object.
        book_id: The ID of the book to delete.
    Returns:
        HttpResponse: Renders 'library/book_confirm_delete.html' or redirects.
    """
    book = get_object_or_404(Book, pk=book_id) # Gets the book to delete or 404.
    if request.method == 'POST':
        book_title = book.title # Get title before deleting
        book.delete() # Deletes the book from the database.
        messages.success(request, f"Book '{book_title}' deleted successfully.")
        return redirect('admin_books') # Redirects to the list of books.
    # For GET request, show a confirmation page.
    return render(request, 'library/book_confirm_delete.html', {'book': book})