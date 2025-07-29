# This file defines the forms used in the 'library' app.
# Forms are used to handle user input and validation.
# This file is crucial for user interactions, such as registration, login, and profile updates.
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Book, Review
import re
from django.core.exceptions import ValidationError


class CharacterVarietyValidator:
    """
    This class is a custom validator for passwords.
    It ensures that the password contains at least one uppercase letter, one lowercase letter, one digit, and one symbol.
    """
    def __call__(self, password):
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.", code='password_no_upper')
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.", code='password_no_lower')
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.", code='password_no_digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one symbol.", code='password_no_symbol')

    def get_help_text(self):
        return "Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one symbol."


class UserRegistrationForm(UserCreationForm):
    """
    This form is used for user registration.
    It inherits from the built-in Django UserCreationForm and adds a date of birth field.
    """
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, 2023)))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one symbol."
        self.fields['password2'].help_text = "Enter the same password as before, for verification."
        self.fields['password1'].validators.append(CharacterVarietyValidator())
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserLoginForm(forms.Form):
    """
    This form is used for user login.
    It has fields for username and password.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserEditForm(forms.ModelForm):
    """
    This form is used for editing a user's profile information.
    It has fields for first name and last name.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True


class UserEditUsernameEmailForm(forms.ModelForm):
    """
    This form is used for editing a user's username and email.
    It requires the user to enter their current password for verification.
    """
    current_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Incorrect password.")
        return current_password


class UserEditPasswordForm(forms.Form):
    """
    This form is used for changing a user's password.
    It requires the user to enter their current password and the new password twice.
    """
    current_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password", help_text="Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one symbol.")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['new_password'].validators.append(CharacterVarietyValidator())
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Incorrect password.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "Passwords don't match.")

        return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data["new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


from .models import Genre

class BookForm(forms.ModelForm):
    """
    This form is used for adding and editing books.
    It has fields for the book's title, author, genres, and other information.
    """
    author_first_name = forms.CharField(max_length=50)
    author_last_name = forms.CharField(max_length=50)
    genre1 = forms.ModelChoiceField(queryset=Genre.objects.all(), required=False)
    genre2 = forms.ModelChoiceField(queryset=Genre.objects.all(), required=False)
    genre3 = forms.ModelChoiceField(queryset=Genre.objects.all(), required=False)

    class Meta:
        model = Book
        exclude = ('authors', 'genres')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ReviewForm(forms.ModelForm):
    """
    This form is used for submitting book reviews.
    It has fields for the review text and rating.
    """
    rating = forms.ChoiceField(choices=[(i, i) for i in range(0, 6)])

    class Meta:
        model = Review
        fields = ['review_text', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
