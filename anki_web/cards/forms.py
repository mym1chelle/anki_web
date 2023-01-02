from django import forms
from .models import Cards
from anki_web.styles.models import Styles


class CreateCardForm(forms.ModelForm):
    class Meta:
        model = Cards
        fields = [
            'question',
            'question_type',
            'answer',
            'answer_type',
            'style',
        ]


class UploadFileForm(forms.Form):
    TYPES = [
        ('md', 'Markdown'),
        ('text', 'Text'),
        ('html', 'HTML')
    ]

    question_type = forms.ChoiceField(
        choices=TYPES,
        widget=forms.Select
    )
    answer_type = forms.ChoiceField(
        choices=TYPES,
        widget=forms.Select
    )

    card_style = forms.ModelChoiceField(queryset=Styles.objects.all(), required=True)
    file = forms.FileField()
