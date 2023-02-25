from django.contrib.auth.models import AbstractUser
from django.db import models
from anki_web.users.constants import (
    USERS_MODEL_VN,
    USERS_MODEL_VN_PLURAL
)


class Users(AbstractUser):
    class Meta:
        verbose_name = USERS_MODEL_VN
        verbose_name_plural = USERS_MODEL_VN_PLURAL

    email = models.EmailField(blank=True, unique=True)
    email_is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username
