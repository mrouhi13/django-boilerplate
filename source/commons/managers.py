from django.db import models

from commons.helpers import get_active_lang


class BaseQueryset(models.QuerySet):

    def active_language(self):
        return self.filter(language=get_active_lang())


class BaseManager(models.Manager):

    def get_queryset(self):
        return BaseQueryset(model=self.model, using=self._db,
                            hints=self._hints)

    def active_language(self):
        return self.get_queryset().active_language()
