# This file contains the tests for the library application.
# It is related to the following files:
# - `views.py`: This file is tested by the view tests in this file.
# - `forms.py`: This file is tested by the form tests in this file.
# - `models.py`: This file is tested by the model tests in this file.

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, date

from .models import Book, Loan, LoanStatus, Author, User
from .views import admin_dashboard
from . import views
from unittest.mock import patch, MagicMock

# Get the custom User model
UserModel = get_user_model()

class AdminDashboardViewTests(TestCase):
    # This class contains the tests for the `admin_dashboard` view.
    def setUp(self):
        # This method is called before each test.
        self.factory = RequestFactory() # Create a request factory.
        self.staff_user = MagicMock(spec=UserModel) # Create a mock staff user.
        self.staff_user.username = 'staffmember' # Set the username of the staff user.
        self.staff_user.is_staff = True # Set the `is_staff` attribute of the staff user to `True`.
        self.staff_user.is_authenticated = True # Set the `is_authenticated` attribute of the staff user to `True`.

    @patch('library.views.Loan.objects.filter')
    def test_admin_dashboard_context_active_loans(self, mock_loan_filter):
        # This test tests that the `active_loans` context variable is correctly processed and passed to the context.
        request = self.factory.get(reverse('admin_dashboard')) # Create a GET request to the `admin_dashboard` view.
        request.user = self.staff_user # Set the user of the request to the staff user.

        # Mock data for active loans
        mock_book1 = MagicMock(spec=Book, title='Active Book 1') # Create a mock book.
        mock_user1 = MagicMock(spec=UserModel, username='borrower1') # Create a mock user.
        mock_loan1 = MagicMock(spec=Loan, book=mock_book1, user=mock_user1,
                               status=LoanStatus.BORROWED, due_date=date.today() + timedelta(days=5),
                               borrow_date=timezone.now(),
                               get_status_display=MagicMock(return_value=LoanStatus.BORROWED.label)) # Create a mock loan.


        mock_qs = MagicMock() # Create a mock queryset.
        mock_qs.select_related.return_value = mock_qs # Configure the mock queryset.
        mock_qs.order_by.return_value = [mock_loan1] # Configure the mock queryset.

        mock_loan_filter.return_value = mock_qs # Configure the mock loan filter.

        # Simulate decorator by calling view directly if user is staff
        if request.user.is_staff:
            response = admin_dashboard(request) # Call the `admin_dashboard` view.
            self.assertEqual(response.status_code, 200) # Check that the status code is 200.
            self.assertIn('active_loans', response.context_data) # Check that the `active_loans` context variable is in the context.
            self.assertEqual(len(response.context_data['active_loans']), 1) # Check that the length of the `active_loans` context variable is 1.
            self.assertEqual(response.context_data['active_loans'][0].book.title, 'Active Book 1') # Check that the title of the first active loan is 'Active Book 1'.
        else:
            self.fail("Test setup error, staff user expected.") # Fail the test if the user is not a staff user.

    @patch('library.views.Loan.objects.filter')
    def test_admin_dashboard_context_overdue_books(self, mock_loan_filter):
        # This test tests that the `overdue_books_with_fines` context variable is correctly processed.
        request = self.factory.get(reverse('admin_dashboard')) # Create a GET request to the `admin_dashboard` view.
        request.user = self.staff_user # Set the user of the request to the staff user.

        today = timezone.now().date() # Get the current date.
        mock_book_overdue = MagicMock(spec=Book, title='Overdue Book 1') # Create a mock book.
        mock_user_overdue = MagicMock(spec=UserModel, username='overdueborrower') # Create a mock user.

        # Loan that is overdue by 5 days
        mock_overdue_loan1 = MagicMock(
            spec=Loan, book=mock_book_overdue, user=mock_user_overdue,
            status=LoanStatus.BORROWED, # Will be caught by due_date__lt=today
            due_date=today - timedelta(days=5),
            borrow_date=timezone.now() - timedelta(days=10)
        )
        # Loan that is marked OVERDUE, also overdue by 2 days
        mock_overdue_loan2 = MagicMock(
            spec=Loan, book=MagicMock(spec=Book, title='Overdue Book 2'), user=mock_user_overdue,
            status=LoanStatus.OVERDUE,
            due_date=today - timedelta(days=2),
            borrow_date=timezone.now() - timedelta(days=7)
        )

        # Configure the mock queryset manager
        # The first call to filter is for active_loans, second for overdue_loans_query
        mock_active_qs = MagicMock() # Create a mock queryset.
        mock_active_qs.select_related.return_value = mock_active_qs # Configure the mock queryset.
        mock_active_qs.order_by.return_value = [] # No active loans for this specific test part

        mock_overdue_qs = MagicMock() # Create a mock queryset.
        mock_overdue_qs.select_related.return_value = mock_overdue_qs # Configure the mock queryset.
        mock_overdue_qs.order_by.return_value = [mock_overdue_loan1, mock_overdue_loan2] # Configure the mock queryset.

        mock_loan_filter.side_effect = [mock_active_qs, mock_overdue_qs] # Configure the mock loan filter.


        response = admin_dashboard(request) # Call the `admin_dashboard` view.
        self.assertEqual(response.status_code, 200) # Check that the status code is 200.
        self.assertIn('overdue_books_with_fines', response.context_data) # Check that the `overdue_books_with_fines` context variable is in the context.

        overdue_data = response.context_data['overdue_books_with_fines'] # Get the `overdue_books_with_fines` context variable.
        self.assertEqual(len(overdue_data), 2) # Check that the length of the `overdue_books_with_fines` context variable is 2.

        # Check first overdue book
        self.assertEqual(overdue_data[0]['loan'].book.title, 'Overdue Book 1') # Check the title of the first overdue book.
        self.assertEqual(overdue_data[0]['days_overdue'], 5) # Check the number of days overdue for the first overdue book.
        self.assertEqual(overdue_data[0]['fine_amount'], 5.00) # Check the fine amount for the first overdue book.

        # Check second overdue book
        self.assertEqual(overdue_data[1]['loan'].book.title, 'Overdue Book 2') # Check the title of the second overdue book.
        self.assertEqual(overdue_data[1]['days_overdue'], 2) # Check the number of days overdue for the second overdue book.
        self.assertEqual(overdue_data[1]['fine_amount'], 2.00) # Check the fine amount for the second overdue book.
        self.assertIn('today', response.context_data) # Check that the `today` context variable is in the context.


class BulkEmailOverdueBorrowersTests(TestCase):
    # This class contains the tests for the `bulk_email_overdue_borrowers` view.
    def setUp(self):
        # This method is called before each test.
        self.factory = RequestFactory() # Create a request factory.
        self.staff_user = MagicMock(spec=UserModel) # Create a mock staff user.
        self.staff_user.username = 'staffmailer' # Set the username of the staff user.
        self.staff_user.email = 'staffmailer@example.com' # Set the email of the staff user.
        self.staff_user.is_staff = True # Set the `is_staff` attribute of the staff user to `True`.
        self.staff_user.is_authenticated = True # Set the `is_authenticated` attribute of the staff user to `True`.


    @patch('library.views.send_mail')
    @patch('library.views.Loan.objects.filter')
    def test_bulk_email_sends_correct_emails(self, mock_loan_filter, mock_send_mail):
        # This test tests that the `bulk_email_overdue_borrowers` view sends the correct emails.
        request = self.factory.post(reverse('send_overdue_emails')) # Create a POST request to the `send_overdue_emails` view.
        request.user = self.staff_user # Set the user of the request to the staff user.

        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', MagicMock()) # Mock session for messages
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        today = timezone.now().date() # Get the current date.

        mock_user1_attrs = {'username': 'userone', 'email': 'userone@example.com', 'first_name': 'User'} # Create a mock user.
        mock_user1 = MagicMock(spec=UserModel, **mock_user1_attrs) # Create a mock user.

        mock_book1 = MagicMock(spec=Book, title='The Great Gatsby') # Create a mock book.
        mock_loan1 = MagicMock(spec=Loan, user=mock_user1, book=mock_book1,
                               status=LoanStatus.BORROWED, due_date=today - timedelta(days=10),
                               get_status_display=MagicMock(return_value=LoanStatus.BORROWED.label)) # Create a mock loan.

        mock_loan_filter.return_value.select_related.return_value = [mock_loan1] # Mock chain

        if request.user.is_staff: # Simulate decorator
            response = views.bulk_email_overdue_borrowers(request) # Call the `bulk_email_overdue_borrowers` view.
            self.assertEqual(response.status_code, 302) # Check that the status code is 302.
            self.assertEqual(response.url, reverse('admin_dashboard')) # Check that the response redirects to the `admin_dashboard` view.
            self.assertEqual(mock_send_mail.call_count, 1) # Check that the `send_mail` function was called once.
            args_user1, _ = mock_send_mail.call_args_list[0] # Get the arguments of the `send_mail` function.
            self.assertIn("Dear User,", args_user1[1]) # Check that the email body contains the correct greeting.
            self.assertIn("Total estimated fine for these books: $10.00", args_user1[1]) # Check that the email body contains the correct total fine.
        else:
            self.fail("Test setup error, staff user expected.") # Fail the test if the user is not a staff user.

    @patch('library.views.send_mail')
    @patch('library.views.Loan.objects.filter')
    def test_bulk_email_no_overdue_books(self, mock_loan_filter, mock_send_mail):
        # This test tests that the `bulk_email_overdue_borrowers` view does not send any emails if there are no overdue books.
        request = self.factory.post(reverse('send_overdue_emails')) # Create a POST request to the `send_overdue_emails` view.
        request.user = self.staff_user # Set the user of the request to the staff user.
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_loan_filter.return_value = [] # No overdue loans

        response = views.bulk_email_overdue_borrowers(request) # Call the `bulk_email_overdue_borrowers` view.
        self.assertEqual(response.status_code, 302) # Check that the status code is 302.
        self.assertEqual(mock_send_mail.call_count, 0) # Check that the `send_mail` function was not called.


class ModelTests(TestCase):
    # This class contains the tests for the models.
    def test_author_str(self):
        # This test tests the `__str__` method of the `Author` model.
        author = Author(first_name='Jane', last_name='Smith') # Create an author.
        self.assertEqual(str(author), 'Jane Smith') # Check that the `__str__` method returns the correct string.


class FormTests(TestCase):
    # This class contains the tests for the forms.
    def test_character_variety_validator(self):
        # This test tests the `CharacterVarietyValidator` validator.
        from .forms import CharacterVarietyValidator
        from django.core.exceptions import ValidationError

        validator = CharacterVarietyValidator() # Create a validator.

        with self.assertRaisesMessage(ValidationError, "Password must contain at least one uppercase letter."):
            validator("password123!") # Check that the validator raises a `ValidationError` if the password does not contain an uppercase letter.
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one lowercase letter."):
            validator("PASSWORD123!") # Check that the validator raises a `ValidationError` if the password does not contain a lowercase letter.
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one digit."):
            validator("PasswordABC!") # Check that the validator raises a `ValidationError` if the password does not contain a digit.
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one symbol."):
            validator("Password123") # Check that the validator raises a `ValidationError` if the password does not contain a symbol.

        # Should pass
        try:
            validator("Password123!") # Check that the validator does not raise a `ValidationError` if the password is valid.
        except ValidationError:
            self.fail("CharacterVarietyValidator failed on a valid password.") # Fail the test if the validator raises a `ValidationError`.
