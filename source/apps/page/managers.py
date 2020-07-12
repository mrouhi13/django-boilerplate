import random

from django.contrib.postgres.search import SearchQuery, SearchRank, \
    SearchVector
from django.db import models

from commons.helpers import get_active_lang
from commons.managers import BaseManager, BaseQueryset


class PageQueryset(BaseQueryset):

    def all_active(self):
        return self.filter(is_active=True, language=get_active_lang())


class GroupManager(models.Manager):

    def is_gid_exist(self, gid):
        return self.filter(gid=gid).exists()


class PageManager(BaseManager):

    def get_queryset(self):
        return PageQueryset(model=self.model, using=self._db,
                            hints=self._hints)

    def all_active(self):
        return self.get_queryset().all_active()

    def search(self, text):
        vector = SearchVector('title', weight='A') + \
                 SearchVector('subtitle', weight='B') + \
                 SearchVector('content', 'event_date', 'image_caption',
                              weight='C')
        query = SearchQuery(text, search_type='plain')
        rank = SearchRank(vector, query)
        return self.all_active().annotate(
            rank=rank).filter(rank__gte=0.01).order_by('-rank')

    def get_random_pages(self):
        all_pages = self.all_active()
        pages_sample_list = list(all_pages.values_list('pk', flat=True))
        max_random_page_count = 3  # TODO: Make this variable dynamic.

        if len(pages_sample_list) < 3:
            max_random_page_count = len(pages_sample_list)

        random_pages_id = random.sample(pages_sample_list,
                                        max_random_page_count)
        random_pages_list = list(all_pages.filter(pk__in=random_pages_id))

        random.shuffle(random_pages_list)

        return random_pages_list

    def is_pid_exist(self, pid):
        return self.filter(pid=pid).exists()
