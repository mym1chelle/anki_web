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

        widgets = {
            'question': forms.Textarea(attrs={
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5 t-resize-none",
                'placeholder': 'Вопрос'
            }),
            'question_type': forms.Select(attrs={
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5 t-resize-none",
            }),
            'answer': forms.Textarea(attrs={
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5 t-resize-none",
                'placeholder': 'Ответ'
            }),
            'answer_type': forms.Select(attrs={
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5 t-resize-none",
            }),
            'style': forms.Select(attrs={
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5 t-resize-none",
            })
        }


class UploadFileForm(forms.Form):
    TYPES = [
        ('text', 'Text'),
        ('md', 'Markdown'),
        ('html', 'HTML')
    ]

    question_type = forms.ChoiceField(
        choices=TYPES,
        widget=forms.Select,
        label='Тип вопроса',
    )
    answer_type = forms.ChoiceField(
        choices=TYPES,
        widget=forms.Select,
        label='Тип ответа'
    )

    card_style = forms.ModelChoiceField(
        queryset=Styles.objects.all(),
        required=True,
        label='Стиль карточки'
    )
    file = forms.FileField(
        label='Файл'
    )
