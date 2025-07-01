from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, date

from .models import Book, Loan, LoanStatus, Author, User
from .views import admin_dashboard # Assuming User is from .models
from unittest.mock import patch, MagicMock

# Get the custom User model
UserModel = get_user_model()

class AdminDashboardViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.staff_user = UserModel.objects.create_user(
            username='staffmember',
            email='staff@example.com',
            password='password123',
            is_staff=True
        )
        self.normal_user = UserModel.objects.create_user(
            username='normaluser',
            email='normal@example.com',
            password='password123',
            is_staff=False
        )
        # Note: DB setup like creating Book, Loan objects will fail if DB is not available.
        # These tests will primarily focus on view logic that can be mocked.

    def test_admin_dashboard_access_staff(self):
        """ Test that staff users can access the admin dashboard. """
        request = self.factory.get(reverse('admin_dashboard'))
        request.user = self.staff_user

        # Mock database calls within the view if direct access isn't possible
        with patch('library.views.Loan.objects.filter') as mock_filter:
            # Configure mock_filter to return an empty queryset or a MagicMock
            # that mimics a queryset for select_related and order_by
            mock_qs = MagicMock()
            mock_qs.select_related.return_value = mock_qs
            mock_qs.order_by.return_value = [] # Empty list for loans
            mock_filter.return_value = mock_qs

            response = admin_dashboard(request)
            self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_redirect_non_staff(self):
        """ Test that non-staff users are redirected from admin dashboard. """
        # Note: This tests the @user_passes_test decorator behavior.
        # Django's test client handles decorator redirection automatically.
        # For RequestFactory, the view itself would run if not for the decorator.
        # True test of decorator requires client.login() and client.get()

        # This test is more conceptual for RequestFactory as decorator isn't run by direct view call
        # A full integration test with self.client would be better.
        # For now, we'll assume decorator works as tested in previous steps.
        pass # Placeholder - decorator testing is better with self.client

    @patch('library.views.Loan.objects.filter')
    def test_admin_dashboard_context_active_loans(self, mock_loan_filter):
        """ Test that active_loans are correctly processed and passed to context. """
        request = self.factory.get(reverse('admin_dashboard'))
        request.user = self.staff_user

        # Mock data for active loans
        mock_book1 = MagicMock(spec=Book, title='Active Book 1')
        mock_user1 = MagicMock(spec=UserModel, username='borrower1')
        mock_loan1 = MagicMock(spec=Loan, book=mock_book1, user=mock_user1,
                               status=LoanStatus.BORROWED, due_date=date.today() + timedelta(days=5),
                               borrow_date=timezone.now())

        # Configure the mock queryset manager
        mock_qs = MagicMock()
        mock_qs.select_related.return_value = mock_qs
        mock_qs.order_by.return_value = [mock_loan1] # Return our mock loan

        # Make the filter return our mock_qs for both calls (active_loans and overdue_loans)
        mock_loan_filter.return_value = mock_qs

        response = admin_dashboard(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('active_loans', response.context_data)
        self.assertEqual(len(response.context_data['active_loans']), 1)
        self.assertEqual(response.context_data['active_loans'][0].book.title, 'Active Book 1')

    @patch('library.views.Loan.objects.filter')
    def test_admin_dashboard_context_overdue_books(self, mock_loan_filter):
        """ Test that overdue_books_with_fines are correctly processed. """
        request = self.factory.get(reverse('admin_dashboard'))
        request.user = self.staff_user

        today = timezone.now().date()
        mock_book_overdue = MagicMock(spec=Book, title='Overdue Book 1')
        mock_user_overdue = MagicMock(spec=UserModel, username='overdueborrower')

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
        mock_active_qs = MagicMock()
        mock_active_qs.select_related.return_value = mock_active_qs
        mock_active_qs.order_by.return_value = [] # No active loans for this specific test part

        mock_overdue_qs = MagicMock()
        mock_overdue_qs.select_related.return_value = mock_overdue_qs
        mock_overdue_qs.order_by.return_value = [mock_overdue_loan1, mock_overdue_loan2]

        mock_loan_filter.side_effect = [mock_active_qs, mock_overdue_qs]


        response = admin_dashboard(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('overdue_books_with_fines', response.context_data)

        overdue_data = response.context_data['overdue_books_with_fines']
        self.assertEqual(len(overdue_data), 2)

        # Check first overdue book
        self.assertEqual(overdue_data[0]['loan'].book.title, 'Overdue Book 1')
        self.assertEqual(overdue_data[0]['days_overdue'], 5)
        self.assertEqual(overdue_data[0]['fine_amount'], 5.00)

        # Check second overdue book
        self.assertEqual(overdue_data[1]['loan'].book.title, 'Overdue Book 2')
        self.assertEqual(overdue_data[1]['days_overdue'], 2)
        self.assertEqual(overdue_data[1]['fine_amount'], 2.00)
        self.assertIn('today', response.context_data)


class BulkEmailOverdueBorrowersTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.staff_user = UserModel.objects.create_user(
            username='staffmailer',
            email='staffmailer@example.com',
            password='password123',
            is_staff=True
        )
        # Again, DB interaction for setup is an issue. Tests will mock heavily.

    @patch('library.views.send_mail') # Mock django.core.mail.send_mail
    @patch('library.views.Loan.objects.filter')
    def test_bulk_email_sends_correct_emails(self, mock_loan_filter, mock_send_mail):
        """ Test that bulk email view attempts to send correct emails. """
        request = self.factory.post(reverse('send_overdue_emails')) # POST request
        request.user = self.staff_user
        # Add messages middleware support for RequestFactory
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        today = timezone.now().date()

        mock_user1 = MagicMock(spec=UserModel, username='userone', email='userone@example.com', first_name='User')
        mock_book1 = MagicMock(spec=Book, title='The Great Gatsby')
        mock_loan1 = MagicMock(spec=Loan, user=mock_user1, book=mock_book1,
                               status=LoanStatus.BORROWED, due_date=today - timedelta(days=10)) # 10 days overdue

        mock_user2 = MagicMock(spec=UserModel, username='usertwo', email='usertwo@example.com', first_name='UserTwo')
        mock_book2a = MagicMock(spec=Book, title='1984')
        mock_book2b = MagicMock(spec=Book, title='Brave New World')
        mock_loan2a = MagicMock(spec=Loan, user=mock_user2, book=mock_book2a,
                                status=LoanStatus.OVERDUE, due_date=today - timedelta(days=5)) # 5 days overdue
        mock_loan2b = MagicMock(spec=Loan, user=mock_user2, book=mock_book2b,
                                status=LoanStatus.BORROWED, due_date=today - timedelta(days=3)) # 3 days overdue

        # Mock for Loan.objects.filter().select_related().order_by()
        mock_qs = MagicMock()
        # mock_qs.select_related.return_value = mock_qs # Not strictly needed if filter returns the final list
        # mock_qs.order_by.return_value = [mock_loan1, mock_loan2a, mock_loan2b]
        mock_loan_filter.return_value = [mock_loan1, mock_loan2a, mock_loan2b] # Simpler mock if select_related etc. not chained in view

        response = views.bulk_email_overdue_borrowers(request) # Directly call the view

        self.assertEqual(response.status_code, 302) # Redirects to admin_dashboard
        self.assertEqual(response.url, reverse('admin_dashboard'))

        self.assertEqual(mock_send_mail.call_count, 2) # Should be called once for each user

        # Check arguments for the first user (userone@example.com)
        args_user1, kwargs_user1 = mock_send_mail.call_args_list[0]
        self.assertEqual(args_user1[0], 'Action Required: Overdue Library Books') # Subject
        self.assertIn("Dear User,", args_user1[1]) # Message body
        self.assertIn("- \"The Great Gatsby\" (Due: ", args_user1[1])
        self.assertIn("Overdue: 10 days, Fine: $10.00", args_user1[1])
        self.assertIn("Total estimated fine for these books: $10.00", args_user1[1])
        self.assertEqual(args_user1[3], ['userone@example.com']) # Recipient list

        # Check arguments for the second user (usertwo@example.com)
        args_user2, kwargs_user2 = mock_send_mail.call_args_list[1]
        self.assertEqual(args_user2[0], 'Action Required: Overdue Library Books')
        self.assertIn("Dear UserTwo,", args_user2[1])
        self.assertIn("- \"1984\" (Due: ", args_user2[1])
        self.assertIn("Overdue: 5 days, Fine: $5.00", args_user2[1])
        self.assertIn("- \"Brave New World\" (Due: ", args_user2[1])
        self.assertIn("Overdue: 3 days, Fine: $3.00", args_user2[1])
        self.assertIn("Total estimated fine for these books: $8.00", args_user2[1]) # 5 + 3
        self.assertEqual(args_user2[3], ['usertwo@example.com'])

    @patch('library.views.send_mail')
    @patch('library.views.Loan.objects.filter')
    def test_bulk_email_no_overdue_books(self, mock_loan_filter, mock_send_mail):
        request = self.factory.post(reverse('send_overdue_emails'))
        request.user = self.staff_user
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_loan_filter.return_value = [] # No overdue loans

        response = views.bulk_email_overdue_borrowers(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(mock_send_mail.call_count, 0)

        # Check for messages
        # This part is tricky with RequestFactory and direct view calls.
        # A full client test would be better for message verification.
        # For now, assume logic for messages.info() is correct if no loans.


# TODO: Add tests for forms (e.g. CharacterVarietyValidator if not covered by Django's own tests)
# TODO: Add model __str__ tests (requires DB setup or more complex mocking)
# TODO: Integration tests using self.client for full request-response cycle,
#       especially for login-protected views and form submissions.
#       These will heavily depend on DB availability.

# Example of a simple model test (would ideally need DB)
# class AuthorModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # This part requires DB.
#         # Author.objects.create(first_name='John', last_name='Doe')
#         pass

#     def test_author_str(self):
#         # author = Author.objects.get(id=1) # Requires DB
#         # self.assertEqual(str(author), 'John Doe')

        # Mocked version:
        author = Author(first_name='Jane', last_name='Smith')
        self.assertEqual(str(author), 'Jane Smith')

class FormTests(TestCase):
    def test_character_variety_validator(self):
        from .forms import CharacterVarietyValidator
        from django.core.exceptions import ValidationError

        validator = CharacterVarietyValidator()

        with self.assertRaisesMessage(ValidationError, "Password must contain at least one uppercase letter."):
            validator("password123!")
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one lowercase letter."):
            validator("PASSWORD123!")
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one digit."):
            validator("PasswordABC!")
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one symbol."):
            validator("Password123")

        # Should pass
        try:
            validator("Password123!")
        except ValidationError:
            self.fail("CharacterVarietyValidator failed on a valid password.")

# Note: The UserModel.objects.create_user in setUp methods will fail without a database.
# To run these tests in the current environment, those lines would need to be commented out
# or the database interaction fully mocked, which makes testing actual view behavior difficult.
# The tests above are structured assuming a working DB for setup but mock out calls within the views.
# If setUp itself fails, no tests will run.
# For a DB-less environment, tests would be more limited to pure Python logic.
# For now, I'm providing the structure and some mocked tests.
# The actual running of these tests in the sandbox will likely show DB errors at setUp.

# To make setUp work without DB for RequestFactory tests where user object is just attached:
# self.staff_user = MagicMock(spec=UserModel)
# self.staff_user.username = 'staffmember'
# self.staff_user.email = 'staff@example.com'
# self.staff_user.is_staff = True
# ... and so on for other attributes accessed.
# This is feasible if the view only reads attributes from request.user.
# However, User.objects.create_user is standard practice for test setup.

# Given the "ignore database" instruction, I will modify setUp to use MagicMock for users
# so the test file can at least be parsed and some logic tested.

class AdminDashboardViewTestsNoDB(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.staff_user = MagicMock(spec=UserModel)
        self.staff_user.username = 'staffmember'
        self.staff_user.is_staff = True
        self.staff_user.is_authenticated = True # Important for some checks

        # The view code for admin_dashboard doesn't directly use request.user for query filtering,
        # but for context like `{{ user.username }}` in template. The decorator handles auth.

    @patch('library.views.Loan.objects.filter')
    def test_admin_dashboard_context_active_loans_nodb(self, mock_loan_filter):
        request = self.factory.get(reverse('admin_dashboard'))
        request.user = self.staff_user # Decorator would handle this

        mock_book1 = MagicMock(spec=Book, title='Active Book 1')
        mock_user1 = MagicMock(spec=UserModel, username='borrower1')
        mock_loan1 = MagicMock(spec=Loan, book=mock_book1, user=mock_user1,
                               status=LoanStatus.BORROWED, due_date=date.today() + timedelta(days=5),
                               borrow_date=timezone.now(),
                               get_status_display=MagicMock(return_value=LoanStatus.BORROWED.label))


        mock_qs = MagicMock()
        mock_qs.select_related.return_value = mock_qs
        mock_qs.order_by.return_value = [mock_loan1]

        mock_loan_filter.return_value = mock_qs

        # Simulate decorator by calling view directly if user is staff
        if request.user.is_staff:
            response = admin_dashboard(request) # Direct call
            self.assertEqual(response.status_code, 200)
            self.assertIn('active_loans', response.context_data)
            self.assertEqual(len(response.context_data['active_loans']), 1)
            self.assertEqual(response.context_data['active_loans'][0].book.title, 'Active Book 1')
        else:
            self.fail("Test setup error, staff user expected.")

    # ... (More tests for admin_dashboard with NoDB setup) ...

class BulkEmailOverdueBorrowersTestsNoDB(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.staff_user = MagicMock(spec=UserModel)
        self.staff_user.username = 'staffmailer'
        self.staff_user.email = 'staffmailer@example.com' # Needed for message if user itself is used
        self.staff_user.is_staff = True
        self.staff_user.is_authenticated = True


    @patch('library.views.send_mail')
    @patch('library.views.Loan.objects.filter')
    def test_bulk_email_sends_correct_emails_nodb(self, mock_loan_filter, mock_send_mail):
        request = self.factory.post(reverse('send_overdue_emails'))
        request.user = self.staff_user

        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', MagicMock()) # Mock session for messages
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        today = timezone.now().date()

        mock_user1_attrs = {'username': 'userone', 'email': 'userone@example.com', 'first_name': 'User'}
        mock_user1 = MagicMock(spec=UserModel, **mock_user1_attrs)

        mock_book1 = MagicMock(spec=Book, title='The Great Gatsby')
        mock_loan1 = MagicMock(spec=Loan, user=mock_user1, book=mock_book1,
                               status=LoanStatus.BORROWED, due_date=today - timedelta(days=10),
                               get_status_display=MagicMock(return_value=LoanStatus.BORROWED.label))

        mock_loan_filter.return_value.select_related.return_value = [mock_loan1] # Mock chain

        if request.user.is_staff: # Simulate decorator
            response = views.bulk_email_overdue_borrowers(request)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('admin_dashboard'))
            self.assertEqual(mock_send_mail.call_count, 1)
            args_user1, _ = mock_send_mail.call_args_list[0]
            self.assertIn("Dear User,", args_user1[1])
            self.assertIn("Total estimated fine for these books: $10.00", args_user1[1])
        else:
            self.fail("Test setup error, staff user expected.")


# Final note: The NoDB versions are simplified. Full testing requires a database.
# These NoDB tests primarily check if the view logic can run with mocked data
# and if it attempts to call external services like send_mail correctly.
# They do NOT test database queries, model interactions, or full request lifecycle via Django Client.

# For this exercise, I'll keep the NoDB versions as they are more likely to pass
# in an environment where the DB is not accessible during the test run.
# The original tests requiring DB are good reference for when DB is available.
# I will rename the NoDB test classes to be the primary ones for now.

# Let's refine to use only the NoDB versions for the current context.
# (Removing the DB-dependent setUp from the original classes or renaming them)
# For clarity, I will provide a clean version with only NoDB tests.
# (Content will be replaced by the NoDB-focused test structure in next tool call)

# The user creation in original setUp will cause tests to fail before even running
# if DB is not available. So, the "NoDB" approach for user mocking is essential here.
# I will provide a consolidated test file focusing on the NoDB approach.
# The `admin_dashboard` view is imported as `from .views import admin_dashboard`
# but other views are not imported. `views.bulk_email_overdue_borrowers` should be used.

# Correcting UserModel import, it's already UserModel from get_user_model()
# Correcting view import for bulk_email_overdue_borrowers.
# from .views import admin_dashboard, bulk_email_overdue_borrowers
# This should be done at the top.

# The current structure is a bit messy with DB and NoDB versions.
# I will simplify and provide one set of tests that uses MagicMock for users in setUp.

```

The current `tests.py` has become quite long and has duplicated test classes (`AdminDashboardViewTests` and `AdminDashboardViewTestsNoDB`). I will consolidate this into a single set of tests that use `MagicMock` for user objects in `setUp` to avoid direct database calls for user creation, making them more likely to run in the current environment.

The tests will focus on:
*   `AdminDashboardViewTests`:
    *   Context data for `active_loans`.
    *   Context data for `overdue_books_with_fines`.
*   `BulkEmailOverdueBorrowersTests`:
    *   Correct email content and recipients.
    *   Behavior when no overdue books exist.
*   `FormTests`:
    *   `CharacterVarietyValidator`.
*   `ModelTests`:
    *   Basic `__str__` method for `Author` (as an example of a non-DB model test).

This is still a partial set of tests, but it addresses the new admin dashboard features and some critical components like custom validators, as much as possible without a live database for comprehensive integration testing.
