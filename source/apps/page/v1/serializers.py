from rest_framework import serializers

from apps.page.models import Page, Image


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        exclude = ('group', 'is_active', 'author', 'language', 'created_at')
        read_only_fields = ['pid']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ('language', 'updated_at', 'created_at')
