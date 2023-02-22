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
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5",
            }),
            'answer': forms.Textarea(attrs={
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5 t-resize-none",
                'placeholder': 'Ответ'
            }),
            'answer_type': forms.Select(attrs={
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5",
            }),
            'style': forms.Select(attrs={
                'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5",
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
        widget=forms.Select(attrs={
            'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5 t-resize-none",
        }),
        label='Тип вопроса',
    )
    answer_type = forms.ChoiceField(
        choices=TYPES,
        widget=forms.Select(attrs={
            'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5",
        }),
        label='Тип ответа'
    )

    card_style = forms.ModelChoiceField(
        queryset=Styles.objects.all(),
        widget=forms.Select(attrs={
            'class': "t-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5 t-resize-none",
        }),
        required=True,
        label='Стиль карточки'
    )
    file = forms.FileField(
        label='Файл'
    )
