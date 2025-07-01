# File: silent_library/library/admin.py
# Purpose: This file is used to register and customize the models from the 'library' app
# with Django's built-in admin interface. By registering models here, they become
# manageable through the web-based admin panel (typically found at /admin/ or, in this
# project, /admin_builtin/). Custom ModelAdmin classes can be defined to control
# how models are displayed (list_display, search_fields, list_filter) and how their
# edit forms behave (inlines, fieldsets, etc.).

from django.contrib import admin # Imports the Django admin module.
from .models import ( # Imports all necessary models from the app's models.py.
    Author, Book, BookAuthor, Genre, BookGenre,
    User, Loan, Fine, Notification, Review
)
# It's good practice to also import and register the custom User model if you have one,
# possibly with a custom UserAdmin class that inherits from django.contrib.auth.admin.UserAdmin.

# Define custom admin classes to enhance the interface for specific models.
# These classes inherit from `admin.ModelAdmin`.

# Inline editing for intermediary models (BookAuthor, BookGenre) on the Book admin page.
# `admin.TabularInline` provides a compact, table-based layout for inline related objects.
# `admin.StackedInline` provides a more spacious, stacked layout.

class BookAuthorInline(admin.TabularInline):
    """
    Allows editing BookAuthor relationships directly within the Book admin page.
    This makes it easy to add/remove authors for a book.
    """
    model = BookAuthor # Specifies the intermediary model for the inline.
    extra = 1  # Provides a default number of empty extra forms for adding new relationships.
    # autocomplete_fields = ['author'] # If Author model has many entries, consider using autocomplete.

class BookGenreInline(admin.TabularInline):
    """
    Allows editing BookGenre relationships directly within the Book admin page.
    This makes it easy to add/remove genres for a book.
    """
    model = BookGenre # Specifies the intermediary model.
    extra = 1
    # autocomplete_fields = ['genre'] # If Genre model has many entries.

# Custom admin configuration for the Book model.
# The `@admin.register(Book)` decorator is a an alternative to `admin.site.register(Book, BookAdmin)`.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Customizes the admin interface for the Book model."""
    # `list_display` specifies which fields to show in the list view of books.
    list_display = ('title', 'isbn', 'total_copies', 'available_copies')
    # `search_fields` enables a search box to search by these fields.
    search_fields = ('title', 'isbn', 'authors__first_name', 'authors__last_name') # Added search by author
    # `list_filter` adds a sidebar for filtering by these fields.
    list_filter = ('genres', 'authors') # Example: filter by genre or author
    # `inlines` allows editing related models (BookAuthor, BookGenre) on the same page as the Book.
    inlines = [BookAuthorInline, BookGenreInline]
    # `autocomplete_fields` can be useful for ForeignKey or ManyToManyFields with many options.
    # e.g., if you didn't use inlines for authors/genres but selected them directly on Book model.
    # autocomplete_fields = ['authors', 'genres'] # This would apply if authors/genres were direct M2M on Book without 'through'.

# Custom admin configuration for the Author model.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Customizes the admin interface for the Author model."""
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')

# Custom admin configuration for the Genre model.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Customizes the admin interface for the Genre model."""
    list_display = ('genre',)
    search_fields = ('genre',)

# Custom admin configuration for the User model.
# If using Django's default User, this would typically inherit from `django.contrib.auth.admin.UserAdmin`.
# Since a custom User model (`library.User`) is defined, this customizes its admin representation.
@admin.register(User)
class UserAdmin(admin.ModelAdmin): # Consider inheriting from `django.contrib.auth.admin.UserAdmin` for more features
    """Customizes the admin interface for the custom User model."""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active') # Common filters for User model.
    # fieldsets = ... # For more complex form layouts, UserAdmin often has predefined fieldsets.

# Custom admin configuration for the Loan model.
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Customizes the admin interface for the Loan model."""
    list_display = ('book', 'user', 'borrow_date', 'due_date', 'return_date', 'status')
    # `search_fields` can span relationships using `__` notation (e.g., 'book__title').
    search_fields = ('book__title', 'user__username', 'user__email')
    list_filter = ('status', 'due_date', 'borrow_date')
    # `date_hierarchy` adds date-based drilldown navigation.
    date_hierarchy = 'borrow_date'
    # `autocomplete_fields` is useful for selecting book and user if there are many.
    autocomplete_fields = ['book', 'user']


# Custom admin configuration for the Fine model.
@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    """Customizes the admin interface for the Fine model."""
    list_display = ('loan', 'fine_amount', 'payment_status', 'fine_date', 'payment_date')
    search_fields = ('loan__book__title', 'loan__user__username')
    list_filter = ('payment_status', 'fine_date')
    date_hierarchy = 'fine_date'
    autocomplete_fields = ['loan']

# Custom admin configuration for the Review model.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Customizes the admin interface for the Review model."""
    list_display = ('book', 'user', 'rating', 'review_date')
    search_fields = ('book__title', 'user__username')
    list_filter = ('rating', 'review_date')
    date_hierarchy = 'review_date'
    autocomplete_fields = ['book', 'user']

# Registering intermediary models (BookAuthor, BookGenre) to be viewable in admin.
# This is often optional if they are primarily managed via inlines on the main models (Book).
# However, registering them makes them directly accessible in the admin index.
@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    """Admin interface for the BookAuthor linking model."""
    list_display = ('book', 'author')
    autocomplete_fields = ['book', 'author'] # Useful for managing these links directly.

@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    """Admin interface for the BookGenre linking model."""
    list_display = ('book', 'genre')
    autocomplete_fields = ['book', 'genre'] # Useful for managing these links directly.


# Register other models that might not need extensive customization but should be accessible.
# `admin.site.register(ModelName)` uses the default ModelAdmin options.
admin.site.register(Notification)
# Note: If a model is registered with `@admin.register()`, it doesn't need to be registered again with `admin.site.register()`.