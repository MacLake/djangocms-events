from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from .models import Calendar, Event


@admin.register(Calendar)
class CalendarAdmin(ModelAdmin):
    readonly_fields = ['ics']
    actions = ['import_ics']

    @admin.action(description=_('Import selected calendars'))
    def import_ics(self, request, queryset):
        for calendar in queryset.all():
            calendar.import_ics()
            messages.success(request, _(f'Calendar {calendar} imported.'))


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display: list[str] = ['begin', 'end', 'name', 'calendar', 'location']
    list_display_links: list[str] = ['name']
    list_filter: list[str] = ['calendar']
