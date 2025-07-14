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
        self.client.login(username='staffmember', password='password123')

    def test_admin_dashboard_access_staff(self):
        """ Test that staff users can access the admin dashboard. """
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_redirect_non_staff(self):
        """ Test that non-staff users are redirected from admin dashboard. """
        self.client.logout()
        self.client.login(username='normaluser', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    @patch('library.views.Loan.objects.filter')
    def test_admin_dashboard_context_active_loans(self, mock_loan_filter):
        """ Test that active_loans are correctly processed and passed to context. """
        mock_book1 = MagicMock(spec=Book, title='Active Book 1')
        mock_user1 = MagicMock(spec=UserModel, username='borrower1')
        mock_loan1 = MagicMock(spec=Loan, book=mock_book1, user=mock_user1,
                               status=LoanStatus.BORROWED, due_date=date.today() + timedelta(days=5),
                               borrow_date=timezone.now())

        mock_qs = MagicMock()
        mock_qs.select_related.return_value = mock_qs
        mock_qs.order_by.return_value = [mock_loan1]

        mock_loan_filter.return_value = mock_qs

        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('active_loans', response.context)
        self.assertEqual(len(response.context['active_loans']), 1)
        self.assertEqual(response.context['active_loans'][0].book.title, 'Active Book 1')

    @patch('library.views.Loan.objects.filter')
    def test_admin_dashboard_context_overdue_books(self, mock_loan_filter):
        """ Test that overdue_books_with_fines are correctly processed. """
        today = timezone.now().date()
        mock_book_overdue = MagicMock(spec=Book, title='Overdue Book 1')
        mock_user_overdue = MagicMock(spec=UserModel, username='overdueborrower')

        mock_overdue_loan1 = MagicMock(
            spec=Loan, book=mock_book_overdue, user=mock_user_overdue,
            status=LoanStatus.BORROWED,
            due_date=today - timedelta(days=5),
            borrow_date=timezone.now() - timedelta(days=10)
        )
        mock_overdue_loan2 = MagicMock(
            spec=Loan, book=MagicMock(spec=Book, title='Overdue Book 2'), user=mock_user_overdue,
            status=LoanStatus.OVERDUE,
            due_date=today - timedelta(days=2),
            borrow_date=timezone.now() - timedelta(days=7)
        )

        mock_active_qs = MagicMock()
        mock_active_qs.select_related.return_value = mock_active_qs
        mock_active_qs.order_by.return_value = []

        mock_overdue_qs = MagicMock()
        mock_overdue_qs.select_related.return_value = mock_overdue_qs
        mock_overdue_qs.order_by.return_value = [mock_overdue_loan1, mock_overdue_loan2]

        mock_loan_filter.side_effect = [mock_active_qs, mock_overdue_qs]

        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('overdue_books_with_fines', response.context)

        overdue_data = response.context['overdue_books_with_fines']
        self.assertEqual(len(overdue_data), 2)

        self.assertEqual(overdue_data[0]['loan'].book.title, 'Overdue Book 1')
        self.assertEqual(overdue_data[0]['days_overdue'], 5)
        self.assertEqual(overdue_data[0]['fine_amount'], 5.00)

        self.assertEqual(overdue_data[1]['loan'].book.title, 'Overdue Book 2')
        self.assertEqual(overdue_data[1]['days_overdue'], 2)
        self.assertEqual(overdue_data[1]['fine_amount'], 2.00)
        self.assertIn('today', response.context)


class BulkEmailOverdueBorrowersTests(TestCase):
    def setUp(self):
        self.staff_user = UserModel.objects.create_user(
            username='staffmailer',
            email='staffmailer@example.com',
            password='password123',
            is_staff=True
        )
        self.client.login(username='staffmailer', password='password123')

    @patch('library.views.send_mass_mail')
    @patch('library.views.Loan.objects.filter')
    def test_bulk_email_sends_correct_emails(self, mock_loan_filter, mock_send_mass_mail):
        """ Test that bulk email view attempts to send correct emails. """
        today = timezone.now().date()

        mock_user1 = MagicMock(spec=UserModel, username='userone', email='userone@example.com', first_name='User')
        mock_book1 = MagicMock(spec=Book, title='The Great Gatsby')
        mock_loan1 = MagicMock(spec=Loan, user=mock_user1, book=mock_book1,
                               status=LoanStatus.BORROWED, due_date=today - timedelta(days=10))

        mock_user2 = MagicMock(spec=UserModel, username='usertwo', email='usertwo@example.com', first_name='UserTwo')
        mock_book2a = MagicMock(spec=Book, title='1984')
        mock_book2b = MagicMock(spec=Book, title='Brave New World')
        mock_loan2a = MagicMock(spec=Loan, user=mock_user2, book=mock_book2a,
                                status=LoanStatus.OVERDUE, due_date=today - timedelta(days=5))
        mock_loan2b = MagicMock(spec=Loan, user=mock_user2, book=mock_book2b,
                                status=LoanStatus.BORROWED, due_date=today - timedelta(days=3))

        mock_qs = MagicMock()
        mock_qs.select_related.return_value = [mock_loan1, mock_loan2a, mock_loan2b]
        mock_loan_filter.return_value = mock_qs

        response = self.client.post(reverse('send_overdue_emails'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('admin_dashboard'))

        self.assertEqual(mock_send_mass_mail.call_count, 1)

        messages_to_send = mock_send_mass_mail.call_args[0][0]
        self.assertEqual(len(messages_to_send), 2)

        email1 = messages_to_send[0]
        self.assertEqual(email1[0], 'Action Required: Overdue Library Books')
        self.assertIn("Dear User,", email1[1])
        self.assertIn("- \"The Great Gatsby\" (Due: ", email1[1])
        self.assertIn("Overdue: 10 days, Fine: $10.00", email1[1])
        self.assertIn("Total estimated fine for these books: $10.00", email1[1])
        self.assertEqual(email1[3], ['userone@example.com'])

        email2 = messages_to_send[1]
        self.assertEqual(email2[0], 'Action Required: Overdue Library Books')
        self.assertIn("Dear UserTwo,", email2[1])
        self.assertIn("- \"1984\" (Due: ", email2[1])
        self.assertIn("Overdue: 5 days, Fine: $5.00", email2[1])
        self.assertIn("- \"Brave New World\" (Due: ", email2[1])
        self.assertIn("Overdue: 3 days, Fine: $3.00", email2[1])
        self.assertIn("Total estimated fine for these books: $8.00", email2[1])
        self.assertEqual(email2[3], ['usertwo@example.com'])

    @patch('library.views.send_mass_mail')
    @patch('library.views.Loan.objects.filter')
    def test_bulk_email_no_overdue_books(self, mock_loan_filter, mock_send_mass_mail):
        mock_loan_filter.return_value.select_related.return_value = []

        response = self.client.post(reverse('send_overdue_emails'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(mock_send_mass_mail.call_count, 0)
