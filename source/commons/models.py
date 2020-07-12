from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from commons.helpers import get_active_lang
from commons.managers import BaseManager


class AbstractBaseModel(models.Model):
    LANGUAGE_CHOICES = settings.LANGUAGES

    language = models.CharField(
        verbose_name=_('Language'),
        max_length=7,
        db_index=True,
        choices=LANGUAGE_CHOICES,
        default=get_active_lang
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated At'),
        auto_now=True
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True
    )

    objects = BaseManager()

    class Meta:
        abstract = True

    def is_updated(self):
        return self.updated_at is not None or self.pk
