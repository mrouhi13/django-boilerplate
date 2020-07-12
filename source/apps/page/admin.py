from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.page.models import Group, Page, Image
from commons.admins import BaseModelAdmin
from commons.editors import PersianEditors


class PageInlineAdmin(admin.TabularInline):
    model = Page
    readonly_fields = ['pid', 'language', 'created_at']
    fields = ['pid', 'language', 'created_at', 'is_active']
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


class ImagesInlineAdmin(admin.TabularInline):
    model = Image
    readonly_fields = ['language', 'created_at']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    readonly_fields = ['gid', 'updated_at', 'created_at']
    fieldsets = [
        [_('Main info'), {'fields': ['gid', 'is_featured']}],
        [_('Important dates'), {'fields': ['updated_at', 'created_at']}]
    ]
    list_display = ['title', 'is_featured', 'updated_at', 'created_at',
                    'in_use']
    list_filter = ['is_featured', 'updated_at', 'created_at']
    search_fields = ['gid', 'pages__pid', 'pages__title']
    inlines = [PageInlineAdmin]

    def in_use(self, obj):
        return bool(obj.page_set.all().count())

    in_use.boolean = True
    in_use.short_description = _('In use?')

    def title(self, obj):
        return obj.__str__()

    title.short_description = _('Title')


@admin.register(Page)
class PageAdmin(BaseModelAdmin):
    date_hierarchy = 'created_at'
    readonly_fields = ['pid', 'updated_at', 'created_at']
    fieldsets = [
        [_('Main info'), {
            'fields': ['pid', 'group', 'title', 'subtitle', 'content',
                       'event_date']
        }],
        [_('Further info'), {
            'classes': ['collapse'],
            'fields': ['reference', 'website', 'wikipedia_link', 'author',
                       'is_active']
        }],
        [_('Important dates'), {'fields': ['updated_at', 'created_at']}]
    ]
    list_display = ['title', 'author', 'created_at', 'is_active']
    list_filter = ['is_active', 'updated_at', 'created_at']
    search_fields = ['group__gid', 'pid', 'title', 'content', 'event_date',
                     'website', 'wikipedia_link', 'author', 'reference']
    autocomplete_fields = ['group']
    inlines = [ImagesInlineAdmin]

    def save_model(self, request, obj, form, change):
        editor = PersianEditors(['space', 'number', 'arabic',
                                 'punctuation_marks'])

        obj.title = editor.run(obj.title)
        obj.subtitle = editor.run(obj.subtitle)
        obj.content = editor.run(obj.content)
        obj.event_date = editor.run(obj.event_date)

        super().save_model(request, obj, form, change)
