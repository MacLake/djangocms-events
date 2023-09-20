from collections.abc import Iterable
from datetime import datetime, timedelta, timezone
from typing import Any

from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.db.models import QuerySet
from django.utils.translation import gettext as _

from .models import CalendarPlugin, Event, EventListPlugin


@plugin_pool.register_plugin
class EventListPluginPublisher(CMSPluginBase):
    model: CMSPlugin = EventListPlugin
    module: str = _('Events')
    name: str = _('Event list')
    render_template: str = 'djangocms_events/event_list_plugin.html'

    cache: bool = False

    def render(self, context, instance, placeholder) -> dict[str, Any]:
        now: datetime = datetime.now(timezone.utc)
        events: Iterable
        events = Event.objects.filter(
            end__gte=now, calendar__in=instance.calendars.all()
        ).order_by('begin')[:instance.number]
        if events.count() < instance.number and instance.also_past_events:
            events = reversed(
                Event.objects.filter(calendar__in=instance.calendars.all()
                                    ).order_by('-begin')[:instance.number]
            )
        corner_labels: bool = settings.DJANGOCMS_EVENTS_CORNER_LABELS if hasattr(
            settings, 'DJANGOCMS_EVENTS_CORNER_LABELS'
        ) else False

        context: dict[str, Any] = super().render(context, instance, placeholder)
        context['events'] = events
        context['corner_labels'] = corner_labels
        return context


@plugin_pool.register_plugin
class CalendarPluginPublisher(CMSPluginBase):
    model: CMSPlugin = CalendarPlugin
    module: str = _('Events')
    name: str = _('Calendar')
    render_template: str = 'djangocms_events/calendar_plugin.html'

    cache: bool = False

    def render(self, context, instance, placeholder) -> dict[str, Any]:

        context: dict[str, Any] = super().render(context, instance, placeholder)

        # We show also past events of the current month and up to 6 d before, which can be shown,
        # subtract a day to make
        # sure that all timezones are included, microseconds can be neglected.
        start_of_this_month_minus_6d: datetime = datetime.now(
            timezone.utc
        ).replace(day=1, hour=0, minute=0, second=0) - timedelta(days=7)
        event_list: QuerySet = Event.objects.filter(
            end__gte=start_of_this_month_minus_6d,
            calendar__in=instance.calendars.all()
        ).order_by('begin')
        context['calendars'] = instance.calendars.all()
        context['event_list'] = event_list
        return context
