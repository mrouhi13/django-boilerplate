from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return self.model.objects.active_language()
