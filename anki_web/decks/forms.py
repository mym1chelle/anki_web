from django import forms
from .models import Decks


class CreateDeskForm(forms.ModelForm):
    class Meta:
        model = Decks
        fields = [
            'name'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5",
                'placeholder': 'Название колоды'
            })
        }
