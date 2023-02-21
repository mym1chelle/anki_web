from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Users


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 't-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-py-2.5', 'type': 'password', 'align': 'center', 'placeholder': 'password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={'class': 't-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5', 'type': 'password', 'align': 'center', 'placeholder': 'password'}),
    )

    class Meta:
        model = Users

        fields = [
            'username',
            'password1',
            'password2'
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5",
                'placeholder': 'username'
            })
        }
