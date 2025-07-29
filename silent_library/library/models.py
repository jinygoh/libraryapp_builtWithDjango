# This file defines the database models for the 'library' app.
# Each class in this file represents a table in the database.
# The models are used to create, retrieve, update, and delete records in the database.
# This file is fundamental to the data structure of the application.
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


# These classes define choices for fields that have a limited set of possible values.
# This is similar to an ENUM in SQL.
class LoanStatus(models.TextChoices):
    """
    Represents the status of a loan.
    """
    BORROWED = 'borrowed', 'Borrowed'
    RETURNED = 'returned', 'Returned'
    OVERDUE = 'overdue', 'Overdue'

class FinePaymentStatus(models.TextChoices):
    """
    Represents the payment status of a fine.
    """
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    WAIVED = 'waived', 'Waived'

class Author(models.Model):
    """
    Represents an author of a book.
    Each author has a first and last name.
    """
    first_name = models.CharField(max_length=50, db_index=True)
    last_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        # This class contains metadata for the model.
        db_table = 'authors' # Explicitly set table name to match SQL
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        # This method defines the string representation of the model.
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    """
    Represents a book in the library.
    Each book has a title, ISBN, and a number of copies.
    """
    title = models.CharField(max_length=200, db_index=True)
    isbn = models.CharField(max_length=17, unique=True)
    total_copies = models.PositiveIntegerField(default=1, db_index=True)
    available_copies = models.PositiveIntegerField(default=1, db_index=True)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)

    # These fields define many-to-many relationships with other models.
    # The 'through' parameter specifies the intermediate model that is used to link the two models.
    authors = models.ManyToManyField(Author, through='BookAuthor')
    genres = models.ManyToManyField('Genre', through='BookGenre')

    class Meta:
        db_table = 'books'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        constraints = [
            # This constraint ensures that the number of available copies is always less than or equal to the total number of copies.
            # SQL CHECK ((`totalCopies` >= 0)) is handled by PositiveIntegerField
            CheckConstraint(
                check=Q(available_copies__lte=F('total_copies')),
                name='available_copies_lte_total_copies',
            )
        ]

    def __str__(self):
        return self.title

class BookAuthor(models.Model):
    """
    This is an intermediate model that links the Book and Author models.
    It represents the relationship between a book and its author.
    """
    book = models.ForeignKey(Book, on_delete=models.RESTRICT) # SQL: ON DELETE RESTRICT
    author = models.ForeignKey(Author, on_delete=models.RESTRICT) # SQL: ON DELETE RESTRICT

    class Meta:
        db_table = 'books_authors'
        verbose_name = 'Book Author'
        verbose_name_plural = 'Book Authors'

    def __str__(self):
        return f"{self.book.title} - {self.author.first_name} {self.author.last_name}"

class Genre(models.Model):
    """
    Represents a genre of a book.
    Each genre has a unique name.
    """
    genre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'genres'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.genre

class BookGenre(models.Model):
    """
    This is an intermediate model that links the Book and Genre models.
    It represents the relationship between a book and its genre.
    """
    book = models.ForeignKey(Book, on_delete=models.RESTRICT) # SQL: ON DELETE RESTRICT
    genre = models.ForeignKey(Genre, on_delete=models.RESTRICT) # SQL: ON DELETE RESTRICT

    class Meta:
        db_table = 'books_genres'
        verbose_name = 'Book Genre'
        verbose_name_plural = 'Book Genres'

    def __str__(self):
        return f"{self.book.title} - {self.genre.genre}"

class User(AbstractUser):
    """
    Represents a user of the library.
    This model extends the built-in Django User model.
    """
    # userID is replaced by the default 'id' AutoField from Django.
    # username, password, email, first_name, last_name are in AbstractUser.
    # is_admin can be represented by is_staff or is_superuser.
    # The old Login model's last_login_timestamp is `last_login` in AbstractUser.
    # The old Login model's registration_date is `date_joined` in AbstractUser.
    date_of_birth = models.DateField(null=True, blank=True, db_index=True)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

class Loan(models.Model):
    """
    Represents a loan of a book to a user.
    Each loan has a borrow date, due date, and return date.
    """
    borrow_date = models.DateTimeField(auto_now_add=True, db_index=True)
    due_date = models.DateField(db_index=True)
    return_date = models.DateField(null=True, blank=True, db_index=True)
    status = models.CharField(
        max_length=10,
        choices=LoanStatus.choices,
        default=LoanStatus.BORROWED,
        db_index=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_index=True) # SQL: ON DELETE RESTRICT
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, db_index=True) # SQL: ON DELETE RESTRICT

    class Meta:
        db_table = 'loans'
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        return f"Loan {self.id} - {self.book.title} to {self.user.username}"

class Fine(models.Model):
    """
    Represents a fine for an overdue loan.
    Each fine has an amount and a payment status.
    """
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=10,
        choices=FinePaymentStatus.choices,
        default=FinePaymentStatus.PENDING,
        db_index=True
    )
    fine_date = models.DateTimeField(auto_now_add=True, db_index=True)
    payment_date = models.DateField(null=True, blank=True, db_index=True)
    loan = models.ForeignKey(Loan, on_delete=models.RESTRICT, db_index=True) # SQL: ON DELETE RESTRICT

    class Meta:
        db_table = 'fines'
        verbose_name = 'Fine'
        verbose_name_plural = 'Fines'

    def __str__(self):
        return f"Fine {self.id} for Loan {self.loan.id}"

class Notification(models.Model):
    """
    Represents a notification for a user.
    Notifications are used to inform users about important events.
    """
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    notification_text = models.CharField(max_length=512)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_index=True) # SQL: ON DELETE RESTRICT

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"Notification {self.id} for {self.user.username}"

class Review(models.Model):
    """
    Represents a review of a book by a user.
    Each review has a rating and a text.
    """
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        db_index=True
    )
    review_text = models.TextField() # SQL: varchar(5000) is large, TextField is more appropriate
    review_date = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_index=True) # SQL: ON DELETE RESTRICT
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, db_index=True) # SQL: No ON DELETE specified, using RESTRICT for consistency

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        # This constraint ensures that the rating is between 1 and 5.
        # SQL CHECK (((`rating` >= 1) and (`rating` <= 5))) is handled by validators

    def __str__(self):
        return f"Review {self.id} for {self.book.title} by {self.user.username}"
