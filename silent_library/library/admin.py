# This file is used to register the models with the Django admin interface.
# The admin interface is a powerful tool that allows you to manage the data in your database.
# This file is related to the `models.py` file because it imports the models from that file.

from django.contrib import admin
from .models import (
    Author, Book, BookAuthor, Genre, BookGenre,
    User, Loan, Fine, Notification, Review
)

# Define custom admin classes to enhance the interface

class BookAuthorInline(admin.TabularInline):
    # This class defines an inline for the `BookAuthor` model.
    # Inlines allow you to edit related models on the same page as the parent model.
    model = BookAuthor # The model to use for the inline.
    extra = 1  # Number of extra forms to display

class BookGenreInline(admin.TabularInline):
    # This class defines an inline for the `BookGenre` model.
    model = BookGenre # The model to use for the inline.
    extra = 1 # Number of extra forms to display

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # This class defines the admin interface for the `Book` model.
    list_display = ('title', 'isbn', 'total_copies', 'available_copies') # The fields to display in the list view.
    search_fields = ('title', 'isbn') # The fields to search on.
    inlines = [BookAuthorInline, BookGenreInline] # The inlines to display on the change page.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # This class defines the admin interface for the `Author` model.
    list_display = ('first_name', 'last_name') # The fields to display in the list view.
    search_fields = ('first_name', 'last_name') # The fields to search on.

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # This class defines the admin interface for the `Genre` model.
    list_display = ('genre',) # The fields to display in the list view.
    search_fields = ('genre',) # The fields to search on.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # This class defines the admin interface for the `User` model.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff') # The fields to display in the list view.
    search_fields = ('username', 'email', 'first_name', 'last_name') # The fields to search on.
    list_filter = ('is_staff',) # The fields to filter on.

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    # This class defines the admin interface for the `Loan` model.
    list_display = ('book', 'user', 'borrow_date', 'due_date', 'status') # The fields to display in the list view.
    search_fields = ('book__title', 'user__email') # The fields to search on.
    list_filter = ('status', 'due_date') # The fields to filter on.

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    # This class defines the admin interface for the `Fine` model.
    list_display = ('loan', 'fine_amount', 'payment_status', 'fine_date') # The fields to display in the list view.
    search_fields = ('loan__book__title', 'loan__user__email') # The fields to search on.
    list_filter = ('payment_status',) # The fields to filter on.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # This class defines the admin interface for the `Review` model.
    list_display = ('book', 'user', 'rating', 'review_date') # The fields to display in the list view.
    search_fields = ('book__title', 'user__email') # The fields to search on.
    list_filter = ('rating',) # The fields to filter on.

@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    # This class defines the admin interface for the `BookAuthor` model.
    list_display = ('book', 'author') # The fields to display in the list view.

@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    # This class defines the admin interface for the `BookGenre` model.
    list_display = ('book', 'genre') # The fields to display in the list view.


# Register other models if they need to be managed
admin.site.register(Notification)