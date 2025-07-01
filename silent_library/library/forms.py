# File: silent_library/library/forms.py
# Purpose: This file defines the forms used in the 'library' application.
# Django forms handle data input, validation, and cleaning. They can be created
# from scratch by inheriting from `forms.Form` or generated automatically from models
# by inheriting from `forms.ModelForm`. These forms are then used in views to
# render HTML input fields and process user-submitted data.

from django import forms # Imports the base forms module.
from django.contrib.auth.forms import UserCreationForm # Imports Django's base form for user registration.
from .models import User, Book, Review # Imports models that these forms will interact with or be based on.
import re # Imports the regular expression module for custom validation.
from django.core.exceptions import ValidationError # Exception raised for validation errors.


# Custom validator class for checking password character variety.
# Validators can be simple functions or callable classes.
class CharacterVarietyValidator:
    """
    A custom validator that checks if a password contains:
    - At least one uppercase letter.
    - At least one lowercase letter.
    - At least one digit.
    - At least one symbol.
    """
    def __call__(self, password):
        """This method is called by Django's form validation system."""
        # `re.search` returns a match object if the pattern is found, otherwise None.
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.", code='password_no_upper')
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.", code='password_no_lower')
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.", code='password_no_digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password): # List of common symbols.
            raise ValidationError("Password must contain at least one symbol.", code='password_no_symbol')

    def get_help_text(self):
        """Returns a help text string describing the password requirements."""
        return "Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one symbol."


# Form for user registration, inheriting from Django's UserCreationForm.
class UserRegistrationForm(UserCreationForm):
    """
    Form for new user registration. Extends Django's UserCreationForm to use
    the custom User model and add custom fields or validation.
    """
    class Meta(UserCreationForm.Meta): # Inherits Meta options from the base UserCreationForm.
        model = User # Specifies that this form is for creating instances of the custom User model.
        # `fields` defines which fields from the User model should be included in the form.
        # Password fields are automatically handled by UserCreationForm.
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth') # Added date_of_birth

    def __init__(self, *args, **kwargs):
        """Initializes the form, adding custom help text, validators, and CSS classes."""
        super().__init__(*args, **kwargs) # Calls the parent class's __init__ method.
        # Add custom help text for password fields.
        self.fields['password1'].help_text = CharacterVarietyValidator().get_help_text() # Use help text from validator
        self.fields['password2'].help_text = "Enter the same password as before, for verification."
        # Add the custom password validator to the 'password1' field.
        self.fields['password1'].validators.append(CharacterVarietyValidator())
        # Add a CSS class 'form-control' to all field widgets for styling (e.g., with Bootstrap).
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'date_of_birth': # Specific widget for date of birth
                field.widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})


# Basic form for user login, inheriting from forms.Form.
class UserLoginForm(forms.Form):
    """Form for user login, with username and password fields."""
    # CharField for username input.
    username = forms.CharField()
    # CharField for password input, using PasswordInput widget to obscure text.
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        """Initializes the form, adding CSS classes to field widgets."""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# ModelForm for editing basic user profile information (first name, last name).
class UserEditForm(forms.ModelForm):
    """Form for editing a user's basic profile information (first_name, last_name)."""
    class Meta:
        model = User # Based on the User model.
        fields = ('first_name', 'last_name') # Only these fields are editable with this form.

    def __init__(self, *args, **kwargs):
        """Initializes the form, adding CSS classes and making fields required."""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True # Makes these fields required in the HTML form.


# ModelForm for editing username and email, requires current password for verification.
class UserEditUsernameEmailForm(forms.ModelForm):
    """Form for editing username and email. Requires current password for security."""
    # Additional field for current password, not part of the User model directly.
    current_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")

    class Meta:
        model = User # Based on the User model.
        fields = ('username', 'email') # Fields to edit.

    def __init__(self, *args, **kwargs):
        """
        Initializes the form. Pops 'user' from kwargs to store the current user instance,
        which is needed for password verification.
        """
        self.user = kwargs.pop('user', None) # Store the user instance passed from the view.
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True

    def clean_current_password(self):
        """
        Custom validation method for the 'current_password' field.
        Checks if the entered current password matches the user's actual password.
        """
        current_password = self.cleaned_data.get('current_password')
        if not self.user or not self.user.check_password(current_password): # Check if user exists and password is correct.
            raise forms.ValidationError("Incorrect password.", code='incorrect_password')
        return current_password # Return the cleaned password.


# Form for changing user password, requires current password and confirmation of new password.
class UserEditPasswordForm(forms.Form):
    """Form for changing a user's password. Requires current and new password confirmation."""
    current_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password",
        help_text=CharacterVarietyValidator().get_help_text() # Use help text from validator
    )
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, *args, **kwargs):
        """
        Initializes the form. Pops 'user' from kwargs for password verification and saving.
        Adds password validator.
        """
        self.user = kwargs.pop('user', None) # Store the user instance.
        super().__init__(*args, **kwargs)
        # Add the custom password validator to the 'new_password' field.
        self.fields['new_password'].validators.append(CharacterVarietyValidator())
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True

    def clean_current_password(self):
        """Validates the 'current_password' field."""
        current_password = self.cleaned_data.get('current_password')
        if not self.user or not self.user.check_password(current_password):
            raise forms.ValidationError("Incorrect password.", code='incorrect_password')
        return current_password

    def clean(self):
        """
        Overall form validation. Checks if 'new_password' and 'confirm_new_password' match.
        This method is called after individual field_clean() methods.
        """
        cleaned_data = super().clean() # Get cleaned data from parent class.
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        # Ensure passwords are provided and match.
        if new_password and confirm_new_password and new_password != confirm_new_password:
            # `self.add_error` links an error to a specific field.
            self.add_error('confirm_new_password', "New passwords don't match.")
            # Alternatively, raise ValidationError for a non-field error that appears at the top of the form.
            # raise forms.ValidationError("New passwords don't match.", code='password_mismatch')

        return cleaned_data # Always return the full cleaned_data dictionary.

    def save(self, commit=True):
        """
        Saves the new password for the user.
        This method is not standard for `forms.Form` but is a common pattern for forms that modify data.
        """
        password = self.cleaned_data["new_password"]
        self.user.set_password(password) # Hashes and sets the new password.
        if commit: # If commit is True (default), save the user model to the database.
            self.user.save(update_fields=['password']) # Only update the password field
        return self.user # Return the user instance.


# ModelForm for creating and editing Book instances.
class BookForm(forms.ModelForm):
    """Form for creating or editing Book instances. Based on the Book model."""
    class Meta:
        model = Book # Specifies the model this form is for.
        fields = '__all__' # Includes all fields from the Book model in the form.
        # Alternatively, list specific fields: fields = ('title', 'isbn', 'authors', 'genres', 'total_copies', 'available_copies')
        # `widgets` can be used here to customize field widgets, e.g., for ManyToManyFields.
        widgets = {
            'authors': forms.CheckboxSelectMultiple, # Example: render authors as checkboxes
            'genres': forms.CheckboxSelectMultiple,  # Example: render genres as checkboxes
        }


    def __init__(self, *args, **kwargs):
        """Initializes the form, adding CSS classes to field widgets."""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # For ManyToMany CheckboxSelectMultiple, 'form-control' might not be ideal.
            # Bootstrap might require custom styling or different widget classes for these.
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                 field.widget.attrs['class'] = 'form-control'
            else:
                # You might want to add specific classes for checkbox groups or remove 'form-control'
                pass


# ModelForm for creating and editing Review instances.
class ReviewForm(forms.ModelForm):
    """Form for creating or editing Review instances. Based on the Review model."""
    class Meta:
        model = Review # Specifies the model.
        # Includes only 'review_text' and 'rating' fields.
        # 'user' and 'book' will be set in the view based on the logged-in user and context.
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}), # Textarea widget for review_text.
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}), # Number input for rating.
        }

    def __init__(self, *args, **kwargs):
        """Initializes the form, adding CSS classes if not already set by widgets Meta."""
        super().__init__(*args, **kwargs)
        # The widgets in Meta already set classes, but this is a fallback or general approach.
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs: # Add class only if not already set
                field.widget.attrs['class'] = 'form-control'
