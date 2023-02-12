from django.db import models
from anki_web.styles.models import Styles
from anki_web.decks.models import Decks
from anki_web.users.models import Users


class Cards(models.Model):

    class Meta:
        ordering = ['random_num']

    TYPES = [
        ('text', 'Text'),
        ('md', 'Markdown'),
        ('html', 'HTML')
    ]

    question = models.TextField(null=False, verbose_name='Вопрос')
    question_type = models.CharField(
        default='text',
        max_length=10,
        choices=TYPES,
        verbose_name='Тип вопроса'
    )
    answer = models.TextField(null=False, verbose_name='Ответ')
    answer_type = models.CharField(
        default='text',
        max_length=10,
        choices=TYPES,
        verbose_name='Тип ответа'
    )
    style = models.ForeignKey(
        Styles,
        on_delete=models.PROTECT,
        verbose_name='Стиль карточки'
    )
    deck = models.ForeignKey(Decks, on_delete=models.PROTECT)
    created_by = models.ForeignKey(Users, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    easiness = models.FloatField(null=True)
    interval = models.IntegerField(null=True)
    repetitions = models.IntegerField(null=True)
    review_date = models.DateField(null=True)
    random_num = models.IntegerField(null=True)

    def __str__(self):
        return self.question
