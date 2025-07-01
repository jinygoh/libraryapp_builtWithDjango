# File: silent_library/library/management/commands/createregistereduser.py
# Purpose: This file defines a custom Django management command `createregistereduser`.
# Management commands allow you to add your own actions that can be run from the command
# line using `python manage.py <command_name>`. This specific command provides an
# interactive way to create a new regular user (not a superuser) with a username,
# email, and password, including basic validation for these fields.
# It uses `getpass` to securely input the password.

from django.core.management.base import BaseCommand, CommandError # Base classes for creating management commands.
# Note: The original import was `from django.contrib.auth.models import User`.
# It should use `settings.AUTH_USER_MODEL` and `get_user_model` for flexibility with custom user models.
from django.contrib.auth import get_user_model # Used to get the active User model.
from django.conf import settings # To access project settings.
from django.core.validators import validate_email # Django's built-in email validator.
from django.core.exceptions import ValidationError # Exception raised by validators.
import getpass # Standard library module for securely getting password input without echoing to the console.

# Get the currently active User model for this project.
User = get_user_model()

class Command(BaseCommand):
    """
    Custom management command to create a new registered user interactively.
    This command prompts for username, email, and password, performs validation,
    and then creates the user.
    """
    # `help` attribute provides a brief description of the command, shown in `python manage.py help`.
    help = 'Creates a new registered user (non-staff, non-superuser) via the console interactively.'

    def handle(self, *args, **options):
        """
        The main logic of the command. This method is executed when the command is run.
        It prompts the user for username, email, and password, validates them,
        and creates a new user.
        """
        # `self.stdout.write` is used for standard output (green for success).
        # `self.stderr.write` is used for error output (red for errors).
        self.stdout.write(self.style.SUCCESS("Create a new registered user"))

        # Loop to get and validate the username.
        while True:
            username = input("Username: ").strip() # Get username input and strip whitespace.
            if not username: # Check if username is empty.
                self.stderr.write(self.style.ERROR("Username cannot be empty."))
                continue # Ask again.
            # Check if the username already exists in the database.
            if User.objects.filter(username=username).exists():
                self.stderr.write(self.style.ERROR(f"Username '{username}' already exists. Please choose another."))
                continue # Ask again.
            break # Username is valid and unique, exit loop.

        # Loop to get and validate the email address.
        while True:
            email = input("Email address: ").strip() # Get email input and strip whitespace.
            if not email: # Check if email is empty.
                self.stderr.write(self.style.ERROR("Email cannot be empty."))
                continue # Ask again.
            try:
                validate_email(email) # Use Django's validator to check email format.
            except ValidationError:
                self.stderr.write(self.style.ERROR("Invalid email address. Please enter a valid email."))
                continue # Ask again.
            # Check if the email already exists in the database.
            if User.objects.filter(email=email).exists():
                self.stderr.write(self.style.ERROR(f"Email '{email}' is already registered. Please use another email."))
                continue # Ask again.
            break # Email is valid and unique, exit loop.

        # Loop to get and validate the password.
        while True:
            # `getpass.getpass()` securely prompts for password without showing it on screen.
            password = getpass.getpass("Password: ")
            if not password: # Check if password is empty.
                self.stderr.write(self.style.ERROR("Password cannot be empty."))
                continue # Ask again.
            password_confirm = getpass.getpass("Password (again): ")
            if password != password_confirm: # Check if passwords match.
                self.stderr.write(self.style.ERROR("Passwords do not match. Please try again."))
                continue # Ask again.

            # TODO: Add password strength validation if desired here.
            # For example, using Django's built-in password validators or a custom one.
            # from django.contrib.auth.password_validation import validate_password
            # try:
            #     validate_password(password)
            # except ValidationError as e:
            #     self.stderr.write(self.style.ERROR("\n".join(e.messages)))
            #     continue
            break # Password is confirmed (and optionally validated), exit loop.

        try:
            # Create the user using the User model's `create_user` method.
            # This method handles password hashing and sets is_staff/is_superuser to False by default.
            user = User.objects.create_user(username=username, email=email, password=password)

            # Optionally, set other fields if your custom User model has them:
            # user.first_name = input("First name (optional): ").strip()
            # user.last_name = input("Last name (optional): ").strip()
            # user.save()

            # Optional: Send a confirmation email here if email services are configured.
            # from django.core.mail import send_mail
            # send_mail(
            #     'Welcome to Silent Library!',
            #     f'Hi {username},\n\nYour account has been successfully created.\n\nThank you,\nThe Silent Library Team',
            #     settings.DEFAULT_FROM_EMAIL, # Use sender from settings
            #     [email],
            #     fail_silently=False, # Raise an error if email sending fails.
            # )
            # self.stdout.write(self.style.SUCCESS("Confirmation email sent."))

            self.stdout.write(self.style.SUCCESS(f"Successfully created user '{username}' with email '{email}'."))
        except Exception as e:
            # If any other error occurs during user creation, raise a CommandError.
            raise CommandError(f"Failed to create user: {e}")
