from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from .models import Users


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={'class': 't-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5', 'type': 'password', 'align': 'center', 'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={'class': 't-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5', 'type': 'password', 'align': 'center', 'placeholder': 'Пароль'}),
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
                'placeholder': 'Имя пользователя'
            })
        }


class LoginUserForm(AuthenticationForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={'class': 't-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5', 'type': 'password', 'align': 'center', 'placeholder': 'Пароль'}),
    )
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5",
                'placeholder': 'Имя пользователя'
            }
        )
    )
