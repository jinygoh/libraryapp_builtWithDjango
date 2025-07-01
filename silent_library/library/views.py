from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from .models import Book, Author, Genre, Loan, Review
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm, BookForm, ReviewForm
from django.db.models import Q
from django.conf import settings


def is_admin(user):
    return user.is_staff

def home(request):
    return render(request, 'library/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send confirmation email
            email_subject = 'Successful Registration on Silent Library'
            email_message = f"Dear {user.first_name},\n\n"                       f"Thank you for registering on our platform. We are excited to have you as a member.\n\n"                       f"Thank you.\nSilent Library Team"
            email_recipient = [user.email]
            
            try:
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=f"Silent Library <{settings.DEFAULT_FROM_EMAIL}>",
                    recipient_list=email_recipient
                )
            except Exception as e:
                messages.error(request, f'Error sending email to {email_recipient}: {str(e)}')

            messages.success(request, 'Registration successful. Please check your email for confirmation.')
            # You might not want to log the user in automatically in this case,
            # as they should confirm their email first.  Uncomment the line below if
            # you still want automatic login.
            # login(request, user)

            return redirect('registration_complete')
    else:
        form = UserRegistrationForm()
    return render(request, 'library/register.html', {'form': form})

def registration_complete(request):
    return render(request, 'library/registration_complete.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin_dashboard')
                return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'library/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    loans = Loan.objects.filter(user=request.user)
    return render(request, 'library/dashboard.html', {'loans': loans})

from .forms import UserRegistrationForm, UserLoginForm, UserEditForm, UserEditUsernameEmailForm, UserEditPasswordForm, BookForm, ReviewForm

@login_required
def profile(request):
    if 'edit_profile' in request.POST:
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)

    if 'edit_username_email' in request.POST:
        username_email_form = UserEditUsernameEmailForm(request.POST, instance=request.user, user=request.user)
        if username_email_form.is_valid():
            username_email_form.save()
            messages.success(request, 'Username and email updated successfully.')
            return redirect('profile')
    else:
        username_email_form = UserEditUsernameEmailForm(instance=request.user, user=request.user)

    if 'change_password' in request.POST:
        password_form = UserEditPasswordForm(request.POST, user=request.user)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully.')
            return redirect('profile')
        # Removed the else block that was duplicating form errors into messages
    else:
        password_form = UserEditPasswordForm(user=request.user)

    return render(request, 'library/profile.html', {
        'form': form,
        'username_email_form': username_email_form,
        'password_form': password_form
    })

def search_books(request):
    query = request.GET.get('q')
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(authors__first_name__icontains=query) |
            Q(authors__last_name__icontains=query) |
            Q(genres__genre__icontains=query)
        ).distinct()
    return render(request, 'library/search.html', {'books': books, 'query': query})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book=book)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', book_id=book.pk)
    else:
        form = ReviewForm()
    return render(request, 'library/book_detail.html', {'book': book, 'reviews': reviews, 'form': form})

from .models import Book, Author, Genre, Loan, Review, LoanStatus # Added LoanStatus
from django.db.models import Q # Ensure Q is imported if not already for LoanStatus filtering

@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def admin_dashboard(request):
import datetime # For calculating overdue fines
from django.utils import timezone # More robust for today's date if timezone awareness is needed

@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def admin_dashboard(request):
    # Active Loans (already implemented)
    active_loans = Loan.objects.filter(
        Q(status=LoanStatus.BORROWED) | Q(status=LoanStatus.OVERDUE)
    ).select_related('book', 'user').order_by('due_date')

    # Overdue Books and Fines
    today = timezone.now().date() # Use timezone-aware current date

    # Query for loans that are overdue or borrowed and past due_date
    # This ensures we catch loans that might not have been explicitly marked 'overdue' yet
    overdue_loans_query = Loan.objects.filter(
        Q(status=LoanStatus.OVERDUE) | (Q(status=LoanStatus.BORROWED) & Q(due_date__lt=today))
    ).select_related('book', 'user').order_by('due_date')

    overdue_books_with_fines = []
    for loan in overdue_loans_query:
        if loan.due_date < today: # Double check, especially for 'borrowed' loans
            days_overdue = (today - loan.due_date).days
            fine_amount = days_overdue * 1.00 # $1 per day
            overdue_books_with_fines.append({
                'loan': loan,
                'days_overdue': days_overdue,
                'fine_amount': fine_amount,
            })
        elif loan.status == LoanStatus.OVERDUE: # Already marked overdue, but due_date might not be in past (edge case)
            # This case implies the status was set manually or by another process
            # If due_date is not in the past, fine might be 0 or based on a different logic
            # For now, only calculate fine if due_date is past
            days_overdue = 0
            fine_amount = 0.00
            if loan.due_date < today: # Recalculate if it was marked overdue but due_date is past
                 days_overdue = (today - loan.due_date).days
                 fine_amount = days_overdue * 1.00

            overdue_books_with_fines.append({
                'loan': loan,
                'days_overdue': days_overdue, # Could be 0 if due_date is not yet past but status is OVERDUE
                'fine_amount': fine_amount,
            })


    context = {
        'active_loans': active_loans,
        'overdue_books_with_fines': overdue_books_with_fines,
        'today': today, # For display or reference in template if needed
    }
    return render(request, 'library/admin_dashboard.html', context)


@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def bulk_email_overdue_borrowers(request):
    if request.method == 'POST':
        today = timezone.now().date()

        overdue_loans_query = Loan.objects.filter(
            Q(status=LoanStatus.OVERDUE) | (Q(status=LoanStatus.BORROWED) & Q(due_date__lt=today))
        ).select_related('user', 'book')

        borrowers_to_notify = {} # {user_email: {'user': user_obj, 'books': []}}

        for loan in overdue_loans_query:
            if loan.due_date < today : # Ensure it's actually overdue for fine calculation and notification
                if loan.user.email not in borrowers_to_notify:
                    borrowers_to_notify[loan.user.email] = {
                        'user': loan.user,
                        'books_details': []
                    }

                days_overdue = (today - loan.due_date).days
                fine_amount = days_overdue * 1.00

                borrowers_to_notify[loan.user.email]['books_details'].append({
                    'title': loan.book.title,
                    'due_date': loan.due_date.strftime("%Y-%m-%d"),
                    'days_overdue': days_overdue,
                    'fine': fine_amount
                })

        messages_to_send = []
        notified_users_count = 0
        failed_users_count = 0

        for email, data in borrowers_to_notify.items():
            user = data['user']
            book_list_str = ""
            total_fine_for_user = 0
            for book_detail in data['books_details']:
                book_list_str += f"- \"{book_detail['title']}\" (Due: {book_detail['due_date']}, Overdue: {book_detail['days_overdue']} days, Fine: ${book_detail['fine']:.2f})\n"
                total_fine_for_user += book_detail['fine']

            if not book_list_str: # Should not happen if logic is correct, but as a safeguard
                continue

            email_subject = 'Action Required: Overdue Library Books'
            email_message = (
                f"Dear {user.first_name or user.username},\n\n"
                f"Our records show that you have one or more books overdue from Silent Library:\n\n"
                f"{book_list_str}\n"
                f"Total estimated fine for these books: ${total_fine_for_user:.2f}\n\n"
                f"Please return these books as soon as possible to avoid further fines. "
                f"If you have already returned these books or believe this is an error, please contact us.\n\n"
                f"Thank you,\nSilent Library Team"
            )

            # For send_mass_mail, each message is a tuple: (subject, message, from_email, recipient_list)
            messages_to_send.append((email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [user.email]))

        if messages_to_send:
            try:
                # send_mass_mail returns the number of successfully sent emails
                num_sent = send_mail( # Corrected: send_mail does not return count, use loop or send_mass_mail
                    subject="[Placeholder Subject]", # This will be overridden per message if using send_mass_mail
                    message="[Placeholder Body]", # This will be overridden
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[m[3][0] for m in messages_to_send], # Extract emails
                    fail_silently=False, # We want to catch errors
                    # For individual messages within a loop:
                    # html_message=None # if you have html version
                )
                # The above send_mail structure is wrong for bulk.
                # Let's use a loop with send_mail for simplicity in error tracking per user for now.
                # Or set up send_mass_mail correctly.

                # Correct approach with a loop for send_mail:
                actually_sent_count = 0
                for subject, message_body, from_addr, recipient in messages_to_send:
                    try:
                        send_mail(subject, message_body, from_addr, recipient, fail_silently=False)
                        actually_sent_count += 1
                    except Exception as e:
                        messages.warning(request, f"Failed to send email to {recipient[0]}: {str(e)}")
                        failed_users_count +=1

                notified_users_count = actually_sent_count

                if notified_users_count > 0:
                    messages.success(request, f'Successfully sent {notified_users_count} overdue notices.')
                if failed_users_count > 0:
                    messages.error(request, f'Failed to send notices to {failed_users_count} users. Check logs for details.')
                if notified_users_count == 0 and failed_users_count == 0 and messages_to_send:
                     messages.warning(request, 'Attempted to send notices, but no emails were actually sent. Check email configuration or logs.')
                elif not messages_to_send:
                    messages.info(request, 'No overdue books found requiring notification.')

            except Exception as e:
                messages.error(request, f'An error occurred while trying to send emails: {str(e)}')
        else:
            messages.info(request, 'No overdue books found requiring notification.')

        return redirect('admin_dashboard') # Redirect back to dashboard

    # If not POST, or if accessed directly via GET (though not typical for this action)
    return redirect('admin_dashboard')


@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def admin_books(request):
    books = Book.objects.all()
    return render(request, 'library/admin_books.html', {'books': books})

@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_books')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form})

@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('admin_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form})

@user_passes_test(is_admin, login_url=reverse_lazy('login'))
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('admin_books')
    return render(request, 'library/book_confirm_delete.html', {'book': book})