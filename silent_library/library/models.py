# This file defines the database models for the library application.
# It is related to other files in the following ways:
# - `admin.py`: This file uses the models defined here to create the admin interface.
# - `views.py`: This file uses the models defined here to retrieve data from the database and render it in templates.
# - `forms.py`: This file uses the models defined here to create forms for creating and updating data.
# - `tests.py`: This file uses the models defined here to create test data.

from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


# Define choices for ENUM fields
class LoanStatus(models.TextChoices):
    # This class defines the choices for the `status` field in the `Loan` model.
    BORROWED = 'borrowed', 'Borrowed'
    RETURNED = 'returned', 'Returned'
    OVERDUE = 'overdue', 'Overdue'

class FinePaymentStatus(models.TextChoices):
    # This class defines the choices for the `payment_status` field in the `Fine` model.
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    WAIVED = 'waived', 'Waived'

class Author(models.Model):
    # This class defines the `Author` model, which represents an author of a book.
    first_name = models.CharField(max_length=50, db_index=True) # The first name of the author.
    last_name = models.CharField(max_length=50, db_index=True) # The last name of the author.

    class Meta:
        # This class defines the metadata for the `Author` model.
        db_table = 'authors' # Explicitly set table name to match SQL
        verbose_name = 'Author' # A human-readable name for the model.
        verbose_name_plural = 'Authors' # The plural version of the human-readable name.

    def __str__(self):
        # This method returns a string representation of the `Author` model.
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    # This class defines the `Book` model, which represents a book in the library.
    title = models.CharField(max_length=200, db_index=True) # The title of the book.
    isbn = models.CharField(max_length=17, unique=True) # The ISBN of the book.
    total_copies = models.PositiveIntegerField(default=1, db_index=True) # The total number of copies of the book.
    available_copies = models.PositiveIntegerField(default=1, db_index=True) # The number of available copies of the book.

    # Many-to-many relationships will be defined later using through models
    authors = models.ManyToManyField(Author, through='BookAuthor') # The authors of the book.
    genres = models.ManyToManyField('Genre', through='BookGenre') # The genres of the book.

    class Meta:
        # This class defines the metadata for the `Book` model.
        db_table = 'books' # Explicitly set table name to match SQL
        verbose_name = 'Book' # A human-readable name for the model.
        verbose_name_plural = 'Books' # The plural version of the human-readable name.
        constraints = [
            # SQL CHECK ((`totalCopies` >= 0)) is handled by PositiveIntegerField
            CheckConstraint(
                check=Q(available_copies__lte=F('total_copies')),
                name='available_copies_lte_total_copies',
            )
        ]

    def __str__(self):
        # This method returns a string representation of the `Book` model.
        return self.title

class BookAuthor(models.Model):
    # This class defines the `BookAuthor` model, which represents the relationship between a book and an author.
    book = models.ForeignKey(Book, on_delete=models.RESTRICT) # SQL: ON DELETE RESTRICT
    author = models.ForeignKey(Author, on_delete=models.RESTRICT) # SQL: ON DELETE RESTRICT

    class Meta:
        # This class defines the metadata for the `BookAuthor` model.
        db_table = 'books_authors' # Explicitly set table name to match SQL
        verbose_name = 'Book Author' # A human-readable name for the model.
        verbose_name_plural = 'Book Authors' # The plural version of the human-readable name.

    def __str__(self):
        # This method returns a string representation of the `BookAuthor` model.
        return f"{self.book.title} - {self.author.first_name} {self.author.last_name}"

class Genre(models.Model):
    # This class defines the `Genre` model, which represents a genre of a book.
    genre = models.CharField(max_length=50, unique=True) # The name of the genre.

    class Meta:
        # This class defines the metadata for the `Genre` model.
        db_table = 'genres' # Explicitly set table name to match SQL
        verbose_name = 'Genre' # A human-readable name for the model.
        verbose_name_plural = 'Genres' # The plural version of the human-readable name.

    def __str__(self):
        # This method returns a string representation of the `Genre` model.
        return self.genre

class BookGenre(models.Model):
    # This class defines the `BookGenre` model, which represents the relationship between a book and a genre.
    book = models.ForeignKey(Book, on_delete=models.RESTRICT) # SQL: ON DELETE RESTRICT
    genre = models.ForeignKey(Genre, on_delete=models.RESTRICT) # SQL: ON DELETE RESTRICT

    class Meta:
        # This class defines the metadata for the `BookGenre` model.
        db_table = 'books_genres' # Explicitly set table name to match SQL
        verbose_name = 'Book Genre' # A human-readable name for the model.
        verbose_name_plural = 'Book Genres' # The plural version of the human-readable name.

    def __str__(self):
        # This method returns a string representation of the `BookGenre` model.
        return f"{self.book.title} - {self.genre.genre}"

class User(AbstractUser):
    # This class defines the `User` model, which represents a user of the library.
    # userID is replaced by the default 'id' AutoField from Django.
    # username, password, email, first_name, last_name are in AbstractUser.
    # is_admin can be represented by is_staff or is_superuser.
    # The old Login model's last_login_timestamp is `last_login` in AbstractUser.
    # The old Login model's registration_date is `date_joined` in AbstractUser.
    date_of_birth = models.DateField(null=True, blank=True, db_index=True) # The date of birth of the user.

    class Meta:
        # This class defines the metadata for the `User` model.
        db_table = 'users' # Explicitly set table name to match SQL
        verbose_name = 'User' # A human-readable name for the model.
        verbose_name_plural = 'Users' # The plural version of the human-readable name.

    def __str__(self):
        # This method returns a string representation of the `User` model.
        return self.username

class Loan(models.Model):
    # This class defines the `Loan` model, which represents a loan of a book to a user.
    borrow_date = models.DateTimeField(auto_now_add=True, db_index=True) # The date the book was borrowed.
    due_date = models.DateField(db_index=True) # The date the book is due.
    return_date = models.DateField(null=True, blank=True, db_index=True) # The date the book was returned.
    status = models.CharField(
        max_length=10,
        choices=LoanStatus.choices,
        default=LoanStatus.BORROWED,
        db_index=True
    ) # The status of the loan.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_index=True) # SQL: ON DELETE RESTRICT
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, db_index=True) # SQL: ON DELETE RESTRICT

    class Meta:
        # This class defines the metadata for the `Loan` model.
        db_table = 'loans' # Explicitly set table name to match SQL
        verbose_name = 'Loan' # A human-readable name for the model.
        verbose_name_plural = 'Loans' # The plural version of the human-readable name.

    def __str__(self):
        # This method returns a string representation of the `Loan` model.
        return f"Loan {self.id} - {self.book.title} to {self.user.username}"

class Fine(models.Model):
    # This class defines the `Fine` model, which represents a fine for an overdue loan.
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2) # The amount of the fine.
    payment_status = models.CharField(
        max_length=10,
        choices=FinePaymentStatus.choices,
        default=FinePaymentStatus.PENDING,
        db_index=True
    ) # The payment status of the fine.
    fine_date = models.DateTimeField(auto_now_add=True, db_index=True) # The date the fine was issued.
    payment_date = models.DateField(null=T`rue, blank=True, db_index=True) # The date the fine was paid.
    loan = models.ForeignKey(Loan, on_delete=models.RESTRICT, db_index=True) # SQL: ON DELETE RESTRICT

    class Meta:
        # This class defines the metadata for the `Fine` model.
        db_table = 'fines' # Explicitly set table name to match SQL
        verbose_name = 'Fine' # A human-readable name for the model.
        verbose_name_plural = 'Fines' # The plural version of the human-readable name.

    def __str__(self):
        # This method returns a string representation of the `Fine` model.
        return f"Fine {self.id} for Loan {self.loan.id}"

class Notification(models.Model):
    # This class defines the `Notification` model, which represents a notification for a user.
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True) # The timestamp of the notification.
    notification_text = models.CharField(max_length=512) # The text of the notification.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_index=True) # SQL: ON DELETE RESTRICT

    class Meta:
        # This class defines the metadata for the `Notification` model.
        db_table = 'notifications' # Explicitly set table name to match SQL
        verbose_name = 'Notification' # A human-readable name for the model.
        verbose_name_plural = 'Notifications' # The plural version of the human-readable name.

    def __str__(self):
        # This method returns a string representation of the `Notification` model.
        return f"Notification {self.id} for {self.user.username}"

class Review(models.Model):
    # This class defines the `Review` model, which represents a review of a book by a user.
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        db_index=True
    ) # The rating of the book, from 1 to 5.
    review_text = models.TextField() # SQL: varchar(5000) is large, TextField is more appropriate
    review_date = models.DateTimeField(auto_now_add=True, db_index=True) # The date the review was written.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_index=True) # SQL: ON DELETE RESTRICT
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, db_index=True) # SQL: No ON DELETE specified, using RESTRICT for consistency

    class Meta:
        # This class defines the metadata for the `Review` model.
        db_table = 'reviews' # Explicitly set table name to match SQL
        verbose_name = 'Review' # A human-readable name for the model.
        verbose_name_plural = 'Reviews' # The plural version of the human-readable name.
        # SQL CHECK (((`rating` >= 1) and (`rating` <= 5))) is handled by validators

    def __str__(self):
        # This method returns a string representation of the `Review` model.
        return f"Review {self.id} for {self.book.title} by {self.user.username}"
