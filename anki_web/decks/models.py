from django.db import models
from anki_web.users.models import Users


class Decks(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        verbose_name='Название колоды'
    )
    created_by = models.ForeignKey(Users, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
