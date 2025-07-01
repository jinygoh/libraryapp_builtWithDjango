# File: silent_library/library/management/commands/seed_data.py
# Purpose: This file defines a custom Django management command `seed_data`.
# This command is designed to populate the database with realistic-looking sample
# data for development and testing purposes. It uses the Faker library to generate
# random data for users, authors, books, genres, loans, fines, notifications, and reviews.
# Running `python manage.py seed_data` will first clear existing data (excluding superusers)
# and then create new sample records.

import random # Standard library for generating random numbers and choices.
from django.core.management.base import BaseCommand # Base class for creating management commands.
from faker import Faker # Library for generating fake data (names, emails, text, etc.).
from django.contrib.auth import get_user_model # Function to get the active User model.
# Imports all necessary models from the 'library' app.
from library.models import Author, Book, BookAuthor, Genre, BookGenre, Loan, Fine, Notification, Review

# Get the currently active User model for this project.
User = get_user_model()

class Command(BaseCommand):
    """
    Custom management command to populate the database with sample data.
    This is useful for creating a development environment with realistic data.
    """
    # `help` attribute provides a brief description of the command.
    help = 'Populates the database with sample data for development and testing.'

    def handle(self, *args, **kwargs):
        """
        The main logic of the command. This method is executed when the command is run.
        It clears existing data (except superusers) and then creates new sample data
        for all relevant models.
        """
        self.stdout.write(self.style.WARNING('Clearing existing data (excluding superusers)...'))
        # Initialize Faker to generate fake data.
        fake = Faker()

        # Clear existing data in a specific order to avoid foreign key constraint issues.
        # Start with models that have foreign keys to others, or that are "leaf" nodes in dependencies.
        Review.objects.all().delete()        # Depends on User, Book
        Notification.objects.all().delete()  # Depends on User
        Fine.objects.all().delete()          # Depends on Loan
        Loan.objects.all().delete()          # Depends on User, Book
        BookGenre.objects.all().delete()     # Depends on Book, Genre (intermediary table)
        BookAuthor.objects.all().delete()    # Depends on Book, Author (intermediary table)
        # Now models that are referenced by the ones above.
        Genre.objects.all().delete()
        Book.objects.all().delete()          # Referenced by BookAuthor, BookGenre, Loan, Review
        Author.objects.all().delete()        # Referenced by BookAuthor
        # Delete all users except superusers to preserve admin access.
        User.objects.exclude(is_superuser=True).delete() # Referenced by Loan, Fine, Notification, Review

        self.stdout.write(self.style.SUCCESS('Existing data cleared. Starting data seeding...'))

        # --- Create Users ---
        self.stdout.write('Creating sample users...')
        users = [] # List to store created user objects for later use.
        for _ in range(10): # Create 10 sample users.
            user = User.objects.create_user( # `create_user` handles password hashing.
                username=fake.unique.user_name(), # Use unique.user_name() to avoid clashes.
                password='password123', # Simple password for development.
                email=fake.unique.email(), # Use unique.email().
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=70) # Generate realistic birth dates.
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f'{len(users)} users created.'))

        # --- Create Authors ---
        self.stdout.write('Creating sample authors...')
        authors = [] # List to store created author objects.
        for _ in range(20): # Create 20 sample authors.
            author = Author.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            authors.append(author)
        self.stdout.write(self.style.SUCCESS(f'{len(authors)} authors created.'))

        # --- Create Genres ---
        self.stdout.write('Creating sample genres...')
        genres = [] # List to store created genre objects.
        predefined_genres = [
            'Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery',
            'Thriller', 'Romance', 'Horror', 'History', 'Biography', 'Poetry',
            'Self-Help', 'Business', 'Technology', 'Travel'
        ]
        for genre_name in predefined_genres:
            genre, created = Genre.objects.get_or_create(genre=genre_name) # Avoids duplicates if run multiple times without clearing.
            genres.append(genre)
        self.stdout.write(self.style.SUCCESS(f'{len(genres)} genres created/retrieved.'))

        # --- Create Books and Link to Authors/Genres ---
        self.stdout.write('Creating sample books and linking them to authors/genres...')
        books = [] # List to store created book objects.
        for i in range(50): # Create 50 sample books.
            total_copies = random.randint(1, 10) # Random number of total copies.
            # Ensure unique ISBNs if Faker might repeat.
            # A simple way is to append loop index or use fake.unique.isbn13() if available and reliable.
            isbn_val = fake.unique.isbn13()
            book = Book.objects.create(
                title=fake.catch_phrase(), # Generate a catchy phrase as title.
                isbn=isbn_val,
                total_copies=total_copies,
                # Available copies should not exceed total copies.
                available_copies=random.randint(0, total_copies)
            )
            books.append(book)

            # Add 1 to 2 authors to each book.
            num_authors = random.randint(1, min(2, len(authors))) # Ensure we don't pick more authors than available
            selected_authors = random.sample(authors, num_authors) # Pick unique authors.
            for author in selected_authors:
                BookAuthor.objects.create(book=book, author=author)

            # Add 1 to 3 genres to each book.
            num_genres = random.randint(1, min(3, len(genres))) # Ensure we don't pick more genres than available
            selected_genres = random.sample(genres, num_genres) # Pick unique genres.
            for genre in selected_genres:
                BookGenre.objects.create(book=book, genre=genre)
        self.stdout.write(self.style.SUCCESS(f'{len(books)} books created and linked.'))

        # --- Create Loans ---
        self.stdout.write('Creating sample loans...')
        loans = [] # List to store created loan objects.
        if users and books: # Ensure there are users and books to create loans for.
            for _ in range(100): # Create 100 sample loans.
                user_choice = random.choice(users)
                book_choice = random.choice(books)

                # Ensure available_copies is decremented if book is borrowed/overdue
                status_choice = random.choice([s[0] for s in Loan._meta.get_field('status').choices]) # Use choices from model

                if book_choice.available_copies > 0 and status_choice in [Loan.LoanStatus.BORROWED, Loan.LoanStatus.OVERDUE]:
                    loan = Loan.objects.create(
                        user=user_choice,
                        book=book_choice,
                        due_date=fake.future_date(end_date='+30d'), # Due date within next 30 days.
                        status=status_choice
                        # borrow_date is auto_now_add
                        # return_date is null by default
                    )
                    loans.append(loan)
                    book_choice.available_copies -= 1
                    book_choice.save(update_fields=['available_copies'])
                elif status_choice == Loan.LoanStatus.RETURNED: # For returned books, don't check/decrement available_copies
                     loan = Loan.objects.create(
                        user=user_choice,
                        book=book_choice,
                        due_date=fake.past_date(start_date='-60d'), # Due date in the past for returned items
                        return_date=fake.past_date(start_date='-30d'), # Return date also in past
                        status=status_choice
                    )
                     loans.append(loan)
            self.stdout.write(self.style.SUCCESS(f'{len(loans)} loans created.'))
        else:
            self.stdout.write(self.style.WARNING('No users or books available to create loans.'))


        # --- Create Fines for Overdue Loans ---
        self.stdout.write('Creating sample fines for overdue loans...')
        fines_created_count = 0
        for loan in loans:
            if loan.status == Loan.LoanStatus.OVERDUE:
                Fine.objects.create(
                    loan=loan,
                    fine_amount=round(random.uniform(1.0, 20.0), 2), # Generate random fine amount.
                    payment_status=random.choice([s[0] for s in Fine._meta.get_field('payment_status').choices])
                    # fine_date is auto_now_add
                    # payment_date is null by default, can be set if status is 'paid'
                )
                fines_created_count += 1
        self.stdout.write(self.style.SUCCESS(f'{fines_created_count} fines created.'))

        # --- Create Notifications ---
        self.stdout.write('Creating sample notifications...')
        notifications_created_count = 0
        if users:
            for user in users:
                for _ in range(random.randint(0, 5)): # Each user gets 0 to 5 notifications.
                    Notification.objects.create(
                        user=user,
                        notification_text=fake.sentence(nb_words=10) # Generate a short sentence.
                        # timestamp is auto_now_add
                    )
                    notifications_created_count += 1
            self.stdout.write(self.style.SUCCESS(f'{notifications_created_count} notifications created.'))
        else:
            self.stdout.write(self.style.WARNING('No users available to create notifications.'))


        # --- Create Reviews ---
        self.stdout.write('Creating sample reviews...')
        reviews_created_count = 0
        if users and books:
            for book_item in books: # Changed variable name to avoid conflict
                for _ in range(random.randint(0, 3)): # Each book gets 0 to 3 reviews.
                    Review.objects.create(
                        user=random.choice(users),
                        book=book_item,
                        rating=random.randint(1, 5), # Rating between 1 and 5.
                        review_text=fake.paragraph(nb_sentences=3) # Generate a short paragraph.
                        # review_date is auto_now_add
                    )
                    reviews_created_count += 1
            self.stdout.write(self.style.SUCCESS(f'{reviews_created_count} reviews created.'))
        else:
            self.stdout.write(self.style.WARNING('No users or books available to create reviews.'))


        self.stdout.write(self.style.SUCCESS('Successfully seeded all data.'))
