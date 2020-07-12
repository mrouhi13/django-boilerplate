from django.contrib import admin
from django.urls import path, include
from django.utils.translation import ugettext_lazy as _
from rest_framework import routers

admin.site.site_header = _('<project_name> administration')
admin.site.site_title = _('<project_name> administration')
admin.site.index_title = _('Dashboard')

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.page.v1.urls', namespace='pages'))
]
