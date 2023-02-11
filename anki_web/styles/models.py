from django.db import models


class Styles(models.Model):
    class Meta:
        verbose_name = 'cтиль'
        verbose_name_plural = 'Стили'

    name = models.CharField(
        max_length=100,
        null=False,
        verbose_name='Название стиля'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
