from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.user.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name=_('Email Address'),
        unique=True,
        error_messages={'unique': _('A user with that email already exists.')}
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.get_username()
