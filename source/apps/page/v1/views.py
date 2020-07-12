from apps.page.v1.serializers import PageSerializer, ImageSerializer
from rest_framework import viewsets

from apps.page.models import Page, Image


class PageViewSet(viewsets.ModelViewSet):
    """Use this endpoint to retrieve pages list/detail."""
    queryset = Page.objects.all_active()
    serializer_class = PageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """Use this endpoint to retrieve images list/detail."""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
