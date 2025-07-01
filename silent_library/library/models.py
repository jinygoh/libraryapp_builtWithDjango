# File: silent_library/library/models.py
# Purpose: This file defines the data models for the 'library' application.
# Each class represents a database table and its attributes represent table columns.
# Django's Object-Relational Mapper (ORM) uses these models to interact with the database,
# allowing database operations to be performed using Python code instead of raw SQL.
# This includes defining relationships between tables (e.g., ForeignKey, ManyToManyField),
# setting constraints, and specifying metadata for how models behave.

from django.db import models # Imports the core models module from Django.
from django.db.models import CheckConstraint, Q, F # For defining database constraints.
    # CheckConstraint: Adds a CHECK constraint to the database table.
    # Q: Used for creating complex database queries, often involving OR conditions.
    # F: Represents the value of a model field in database queries, allowing referencing other fields on the same model.
from django.contrib.auth.models import AbstractUser # Base class for creating a custom user model.
from django.conf import settings # Allows access to project settings, often used for AUTH_USER_MODEL.
from django.core.validators import MinValueValidator, MaxValueValidator # Validators for model fields.


# Define choices for ENUM-like fields using Django's TextChoices.
# This provides a readable way to define a set of allowed string values for a field.

class LoanStatus(models.TextChoices):
    """Defines the possible statuses for a loan."""
    BORROWED = 'borrowed', 'Borrowed' # Value stored in DB, Human-readable name
    RETURNED = 'returned', 'Returned'
    OVERDUE = 'overdue', 'Overdue'

class FinePaymentStatus(models.TextChoices):
    """Defines the possible payment statuses for a fine."""
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    WAIVED = 'waived', 'Waived'

# Model representing an author.
class Author(models.Model):
    """Represents an author of a book."""
    # CharField for the author's first name, max length 50 characters.
    # db_index=True creates a database index on this field for faster queries.
    first_name = models.CharField(max_length=50, db_index=True)
    # CharField for the author's last name.
    last_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        """Metadata options for the Author model."""
        db_table = 'authors' # Explicitly sets the database table name to 'authors'.
        verbose_name = 'Author' # Singular human-readable name for the model (used in Django admin).
        verbose_name_plural = 'Authors' # Plural human-readable name.

    def __str__(self):
        """String representation of an Author object, used in Django admin and debugging."""
        return f"{self.first_name} {self.last_name}" # Returns the full name of the author.

# Model representing a book.
class Book(models.Model):
    """Represents a book in the library."""
    # CharField for the book's title, max length 200 characters. Indexed for faster lookups.
    title = models.CharField(max_length=200, db_index=True)
    # CharField for the ISBN (International Standard Book Number).
    # unique=True ensures that each ISBN is unique in the database.
    isbn = models.CharField(max_length=17, unique=True)
    # PositiveIntegerField for the total number of copies of this book. Defaults to 1. Indexed.
    total_copies = models.PositiveIntegerField(default=1, db_index=True)
    # PositiveIntegerField for the number of currently available copies. Defaults to 1. Indexed.
    available_copies = models.PositiveIntegerField(default=1, db_index=True)

    # ManyToManyField defines a many-to-many relationship with the Author model.
    # `through='BookAuthor'` specifies that an intermediary model `BookAuthor` will be used
    # to manage this relationship (allowing extra data on the relationship if needed).
    authors = models.ManyToManyField(Author, through='BookAuthor')
    # ManyToManyField defines a many-to-many relationship with the Genre model.
    # `through='BookGenre'` specifies the intermediary model `BookGenre`.
    genres = models.ManyToManyField('Genre', through='BookGenre') # 'Genre' as a string to avoid circular import if Genre is defined later.

    class Meta:
        """Metadata options for the Book model."""
        db_table = 'books' # Explicitly sets the database table name.
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        constraints = [
            # PositiveIntegerField already ensures total_copies >= 0.
            # CheckConstraint ensures that `available_copies` is less than or equal to `total_copies`.
            CheckConstraint(
                check=Q(available_copies__lte=F('total_copies')), # The condition to check.
                name='available_copies_lte_total_copies', # Name for this constraint in the database.
            )
        ]

    def __str__(self):
        """String representation of a Book object."""
        return self.title # Returns the title of the book.

# Intermediary model for the many-to-many relationship between Book and Author.
class BookAuthor(models.Model):
    """Intermediary model linking Books and Authors (Many-to-Many relationship)."""
    # ForeignKey to the Book model.
    # on_delete=models.RESTRICT prevents deletion of a Book if it's referenced by a BookAuthor entry.
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    # ForeignKey to the Author model.
    # on_delete=models.RESTRICT prevents deletion of an Author if referenced.
    author = models.ForeignKey(Author, on_delete=models.RESTRICT)

    class Meta:
        """Metadata options for the BookAuthor model."""
        db_table = 'books_authors' # Table name for the Book-Author link.
        verbose_name = 'Book Author Link' # Changed for clarity in admin.
        verbose_name_plural = 'Book Author Links'

    def __str__(self):
        """String representation of a BookAuthor link."""
        return f"{self.book.title} - {self.author.first_name} {self.author.last_name}"

# Model representing a genre.
class Genre(models.Model):
    """Represents a genre for books."""
    # CharField for the genre name, max length 50.
    # unique=True ensures each genre name is unique.
    genre = models.CharField(max_length=50, unique=True)

    class Meta:
        """Metadata options for the Genre model."""
        db_table = 'genres'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        """String representation of a Genre object."""
        return self.genre # Returns the genre name.

# Intermediary model for the many-to-many relationship between Book and Genre.
class BookGenre(models.Model):
    """Intermediary model linking Books and Genres (Many-to-Many relationship)."""
    # ForeignKey to the Book model. on_delete=models.RESTRICT.
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    # ForeignKey to the Genre model. on_delete=models.RESTRICT.
    genre = models.ForeignKey(Genre, on_delete=models.RESTRICT)

    class Meta:
        """Metadata options for the BookGenre model."""
        db_table = 'books_genres' # Table name for the Book-Genre link.
        verbose_name = 'Book Genre Link' # Changed for clarity in admin.
        verbose_name_plural = 'Book Genre Links'

    def __str__(self):
        """String representation of a BookGenre link."""
        return f"{self.book.title} - {self.genre.genre}"

# Custom User model, inheriting from Django's AbstractUser.
# This allows adding custom fields to the standard User model.
class User(AbstractUser):
    """Custom user model for the application. Extends Django's AbstractUser."""
    # AbstractUser already provides: username, password, email, first_name, last_name,
    # is_staff, is_active, is_superuser, last_login, date_joined.
    # The 'id' field is also automatically provided as a primary key.

    # Additional custom field for the user's date of birth.
    # DateField stores a date.
    # null=True allows this field to be NULL in the database.
    # blank=True allows this field to be blank in forms.
    # db_index=True creates a database index on this field.
    date_of_birth = models.DateField(null=True, blank=True, db_index=True)

    class Meta:
        """Metadata options for the custom User model."""
        db_table = 'users' # Explicitly sets the database table name.
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """String representation of a User object."""
        return self.username # Returns the username.

# Model representing a loan of a book to a user.
class Loan(models.Model):
    """Represents a loan of a book to a user."""
    # DateTimeField for the date and time the book was borrowed.
    # auto_now_add=True automatically sets this field to the current datetime when a Loan object is first created.
    borrow_date = models.DateTimeField(auto_now_add=True, db_index=True)
    # DateField for the due date of the loan. Indexed.
    due_date = models.DateField(db_index=True)
    # DateField for the actual return date. Can be null (if not yet returned) and blank in forms. Indexed.
    return_date = models.DateField(null=True, blank=True, db_index=True)
    # CharField for the status of the loan.
    # Uses choices from the LoanStatus TextChoices class defined above.
    # default sets the default status to 'borrowed'. Indexed.
    status = models.CharField(
        max_length=10, # Max length should accommodate the longest choice value.
        choices=LoanStatus.choices,
        default=LoanStatus.BORROWED,
        db_index=True
    )
    # ForeignKey to the User model (using settings.AUTH_USER_MODEL to refer to the custom User model).
    # on_delete=models.RESTRICT prevents deleting a User if they have active loans. Indexed.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_index=True)
    # ForeignKey to the Book model.
    # on_delete=models.RESTRICT prevents deleting a Book if it's part of an active loan. Indexed.
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, db_index=True)

    class Meta:
        """Metadata options for the Loan model."""
        db_table = 'loans'
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        """String representation of a Loan object."""
        return f"Loan {self.id} - {self.book.title} to {self.user.username}"

# Model representing a fine incurred by a user for a loan.
class Fine(models.Model):
    """Represents a fine associated with a loan."""
    # DecimalField for the amount of the fine.
    # max_digits specifies the total number of digits allowed.
    # decimal_places specifies the number of digits after the decimal point.
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # CharField for the payment status of the fine.
    # Uses choices from FinePaymentStatus. Defaults to 'pending'. Indexed.
    payment_status = models.CharField(
        max_length=10, # Max length for choice values.
        choices=FinePaymentStatus.choices,
        default=FinePaymentStatus.PENDING,
        db_index=True
    )
    # DateTimeField for when the fine was issued. Automatically set on creation. Indexed.
    fine_date = models.DateTimeField(auto_now_add=True, db_index=True)
    # DateField for when the fine was paid. Can be null and blank. Indexed.
    payment_date = models.DateField(null=True, blank=True, db_index=True)
    # ForeignKey to the Loan model, indicating which loan this fine is associated with.
    # on_delete=models.RESTRICT prevents deleting a Loan if it has associated fines. Indexed.
    loan = models.ForeignKey(Loan, on_delete=models.RESTRICT, db_index=True)

    class Meta:
        """Metadata options for the Fine model."""
        db_table = 'fines'
        verbose_name = 'Fine'
        verbose_name_plural = 'Fines'

    def __str__(self):
        """String representation of a Fine object."""
        return f"Fine {self.id} for Loan {self.loan.id}"

# Model representing a notification sent to a user.
class Notification(models.Model):
    """Represents a notification for a user."""
    # DateTimeField for when the notification was created. Automatically set. Indexed.
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    # CharField for the text content of the notification. Max length 512.
    notification_text = models.CharField(max_length=512)
    # ForeignKey to the User model, indicating who this notification is for.
    # on_delete=models.RESTRICT. Indexed.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_index=True)

    class Meta:
        """Metadata options for the Notification model."""
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        """String representation of a Notification object."""
        return f"Notification {self.id} for {self.user.username}"

# Model representing a review of a book by a user.
class Review(models.Model):
    """Represents a user's review of a book."""
    # IntegerField for the rating given in the review.
    # `validators` ensures the rating is between 1 and 5 (inclusive). Indexed.
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        db_index=True
    )
    # TextField for the text content of the review. TextField is suitable for longer text.
    # The original SQL `varchar(5000)` is large, TextField is more appropriate as it often maps to TEXT types in SQL.
    review_text = models.TextField()
    # DateTimeField for when the review was submitted. Automatically set on creation. Indexed.
    review_date = models.DateTimeField(auto_now_add=True, db_index=True)
    # ForeignKey to the User model, indicating who wrote the review.
    # on_delete=models.RESTRICT. Indexed.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_index=True)
    # ForeignKey to the Book model, indicating which book is being reviewed.
    # on_delete=models.RESTRICT. Indexed.
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, db_index=True)

    class Meta:
        """Metadata options for the Review model."""
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        # The SQL CHECK constraint for rating (1 to 5) is handled by the MinValueValidator and MaxValueValidator
        # on the `rating` field at the Django level. Django will validate this before saving.
        # If database-level enforcement is still desired, a CheckConstraint could be added here as well.

    def __str__(self):
        """String representation of a Review object."""
        return f"Review {self.id} for {self.book.title} by {self.user.username}"
