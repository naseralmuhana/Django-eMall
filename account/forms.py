from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm 
from account import models as account_models


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = account_models.UserRegistration
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]


class CustomPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(
        label="Enter your email address",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        required=False,
    )
