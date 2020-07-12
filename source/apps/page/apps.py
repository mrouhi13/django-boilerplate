from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PagesConfig(AppConfig):
    name = 'apps.page'
    verbose_name = _('Pages')