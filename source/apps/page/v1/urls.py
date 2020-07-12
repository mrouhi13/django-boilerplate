from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.page.v1.views import PageViewSet, ImageViewSet

app_name = 'page'

router = DefaultRouter()

router.register('pages', PageViewSet)
router.register('images', ImageViewSet)


urlpatterns = [
    path('v1/', include(router.urls))
]
