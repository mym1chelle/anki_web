from django import forms
from .models import Decks


class CreateDeskForm(forms.ModelForm):
    class Meta:
        model = Decks
        fields = [
            'name'
        ]
