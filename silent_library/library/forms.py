# This file defines the forms used in the library application.
# It is related to the following files:
# - `views.py`: This file uses the forms defined here to handle user input.
# - `models.py`: This file uses the models defined here to create the forms.
# - `templates/`: The templates in this directory render the forms defined here.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Book, Review
import re
from django.core.exceptions import ValidationError


class CharacterVarietyValidator:
    # This class is a validator that checks if a password contains at least one uppercase letter, one lowercase letter, one digit, and one symbol.
    def __call__(self, password):
        # This method is called when the validator is used.
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.", code='password_no_upper')
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.", code='password_no_lower')
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.", code='password_no_digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one symbol.", code='password_no_symbol')

    def get_help_text(self):
        # This method returns the help text for the validator.
        return "Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one symbol."


class UserRegistrationForm(UserCreationForm):
    # This class defines the form for user registration.
    class Meta(UserCreationForm.Meta):
        # This class defines the metadata for the form.
        model = User # The model to use for the form.
        fields = ('username', 'email', 'first_name', 'last_name') # The fields to include in the form.

    def __init__(self, *args, **kwargs):
        # This method is called when the form is initialized.
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one symbol."
        self.fields['password2'].help_text = "Enter the same password as before, for verification."
        self.fields['password1'].validators.append(CharacterVarietyValidator())
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserLoginForm(forms.Form):
    # This class defines the form for user login.
    username = forms.CharField() # The username field.
    password = forms.CharField(widget=forms.PasswordInput) # The password field.

    def __init__(self, *args, **kwargs):
        # This method is called when the form is initialized.
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserEditForm(forms.ModelForm):
    # This class defines the form for editing a user's first and last name.
    class Meta:
        # This class defines the metadata for the form.
        model = User # The model to use for the form.
        fields = ('first_name', 'last_name') # The fields to include in the form.

    def __init__(self, *args, **kwargs):
        # This method is called when the form is initialized.
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True


class UserEditUsernameEmailForm(forms.ModelForm):
    # This class defines the form for editing a user's username and email.
    current_password = forms.CharField(widget=forms.PasswordInput, label="Current Password") # The current password field.

    class Meta:
        # This class defines the metadata for the form.
        model = User # The model to use for the form.
        fields = ('username', 'email') # The fields to include in the form.

    def __init__(self, *args, **kwargs):
        # This method is called when the form is initialized.
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True

    def clean_current_password(self):
        # This method is called to clean the current password field.
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Incorrect password.")
        return current_password


class UserEditPasswordForm(forms.Form):
    # This class defines the form for editing a user's password.
    current_password = forms.CharField(widget=forms.PasswordInput, label="Current Password") # The current password field.
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password", help_text="Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one symbol.") # The new password field.
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password") # The confirm new password field.

    def __init__(self, *args, **kwargs):
        # This method is called when the form is initialized.
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['new_password'].validators.append(CharacterVarietyValidator())
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True

    def clean_current_password(self):
        # This method is called to clean the current password field.
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Incorrect password.")
        return current_password

    def clean(self):
        # This method is called to clean the form data.
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "Passwords don't match.")

        return cleaned_data

    def save(self, commit=True):
        # This method is called to save the form data.
        password = self.cleaned_data["new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class BookForm(forms.ModelForm):
    # This class defines the form for creating and editing a book.
    class Meta:
        # This class defines the metadata for the form.
        model = Book # The model to use for the form.
        fields = '__all__' # The fields to include in the form.

    def __init__(self, *args, **kwargs):
        # This method is called when the form is initialized.
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ReviewForm(forms.ModelForm):
    # This class defines the form for creating and editing a review.
    class Meta:
        # This class defines the metadata for the form.
        model = Review # The model to use for the form.
        fields = ['review_text', 'rating'] # The fields to include in the form.
