import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.page.managers import PageManager, GroupManager
from commons.helpers import id_generator, get_active_lang
from commons.models import AbstractBaseModel


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = str(uuid.uuid4()).replace('-', '')
    return f'images/{instance.page.pid}/{new_filename}.{ext}'


def generate_gid():
    new_gid = None
    while not new_gid:
        gid_postfix = id_generator()
        new_gid = f'{settings.GID_PREFIX}_{gid_postfix}'
        if Group.objects.is_gid_exist(new_gid):
            new_gid = None

    return new_gid


def generate_pid():
    new_pid = None
    while not new_pid:
        pid_postfix = id_generator()
        new_pid = f'{settings.PID_PREFIX}_{pid_postfix}'
        if Page.objects.is_pid_exist(new_pid):
            new_pid = None
    return new_pid


class Group(AbstractBaseModel):
    language = None
    gid = models.CharField(
        verbose_name=_('Global ID'),
        max_length=16,
        primary_key=True,
        default=generate_gid,
        db_index=True,
        editable=False
    )
    is_featured = models.BooleanField(
        verbose_name=_('Featured?'),
        default=False
    )

    objects = GroupManager()

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    def __str__(self):
        page = self.page_set.filter(language=get_active_lang()).first()
        return page.title if page else self.gid


class Page(AbstractBaseModel):
    group = models.ForeignKey(
        to=Group,
        to_field='gid',
        verbose_name=_('Group'),
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    pid = models.CharField(
        verbose_name=_('Public ID'),
        max_length=16,
        unique=True,
        default=generate_pid,
        db_index=True
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=128,
        db_index=True
    )
    subtitle = models.CharField(
        verbose_name=_('Subtitle'),
        max_length=128,
        blank=True,
        db_index=True
    )
    content = models.TextField(
        verbose_name=_('Content'),
        max_length=1024,
        blank=True,
        db_index=True
    )
    event_date = models.CharField(
        verbose_name=_('Event Date'),
        max_length=128,
        blank=True,
        help_text=_('Date of an important event for the subject '
                    'entered along with the place of occurrence.'),
        db_index=True
    )
    reference = models.CharField(
        verbose_name=_('Reference'),
        max_length=128,
        blank=True,
        help_text=_('The name of the book, newspaper, magazine or website '
                    'address, blog and... along with the author\'s name.')
    )
    website = models.URLField(
        verbose_name=_('Website'),
        blank=True
    )
    wikipedia_link = models.URLField(
        verbose_name=_('Wikipedia Link'),
        blank=True
    )
    author = models.EmailField(
        verbose_name=_('Author Email'),
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_('Active Status'),
        default=False,
        help_text=_('Designate whether this page can include in the result '
                    'list.')
    )

    objects = PageManager()

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        unique_together = ('group', 'language')

    def __str__(self):
        return self.title


class Image(AbstractBaseModel):
    page = models.ForeignKey(
        to=Page,
        to_field='pid',
        verbose_name=_('Page'),
        on_delete=models.CASCADE
    )
    file = models.ImageField(
        verbose_name=_('Image'),
        upload_to=upload_to,
    )
    caption = models.CharField(
        verbose_name=_('Image Caption'),
        max_length=128,
        blank=True,
        db_index=True,
        help_text=_('A brief description of the location and history of the '
                    'photo.')
    )

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return self.file.name
