from datetime import datetime, timedelta, timezone
from typing import Any

from arrow import Arrow
from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from ics import Calendar as ICSCalendar

from .models import Calendar, Event


def import_calendars(
    request: HttpRequest, start_after_date: Arrow = None
) -> HttpResponse:
    """
    Import all published calendars with a URL of an ics file with the ics lib
    and then create Django Event objects
    """
    ics_calendars: list[ICSCalendar] = []
    calendar: Calendar
    for calendar in Calendar.objects.filter(publish=True).exclude(url=''):
        ics_calendars.append(
            calendar.import_ics(start_after_date=start_after_date)
        )

    context: dict[str, Any] = {'calendars': ics_calendars}
    return render(request, 'djangocms_events/calendar_import.html', context)


class EventListView(ListView):
    """"Show a list of all events of published calendars"""
    model = Event
    paginate_by: int = getattr(settings, 'DJANGOCMS_EVENTS_PAGINATE_BY', 100)
    nr_initially_shown: int = getattr(
        settings, 'DJANGOCMS_EVENTS_NR_INITIALLY_SHOWN', paginate_by
    )
    corner_labels: bool = getattr(
        settings, 'DJANGOCMS_EVENTS_CORNER_LABELS', False
    )
    queryset_calendar: QuerySet = Event.objects.all()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['set'] = 'all'
        context['calendars'] = Calendar.objects.filter(publish=True)
        context['all_events'] = Event.objects.all()
        context['show_month_week_day_control'] = getattr(
            settings, 'DJANGOCMS_EVENTS_SHOW_CALENDAR_MONTH_WEEK_DAY_CONTROL',
            True
        )
        context['nr_initially_shown'] = self.nr_initially_shown
        context['slice_2'] = f'{self.nr_initially_shown}:'
        context['corner_labels'] = self.corner_labels
        context['event_list_calendar'] = self.queryset_calendar

        return context


class FutureEventListView(EventListView):
    """"
    Show a list of all future events of published calendars and those of the last month
    This might save a lot of time when there are many events in the past.
    """
    start_of_this_month_minus_6d: datetime = datetime.now(
        timezone.utc
    ).replace(day=1, hour=0, minute=0, second=0) - timedelta(days=7)
    queryset: QuerySet = Event.objects.filter(
        end__gte=datetime.now(timezone.utc)
    ).order_by('begin')
    queryset_calendar: QuerySet = Event.objects.filter(
        end__gte=start_of_this_month_minus_6d
    ).order_by('begin')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['set'] = 'future'
        context['event_list_calendar'] = self.queryset_calendar
        return context


class PastEventListView(EventListView):
    """Show a list of all past events of published calendars """
    now: datetime = datetime.now(timezone.utc)
    queryset: QuerySet = Event.objects.filter(end__lte=now)
    queryset_calendar: QuerySet = queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['set'] = 'past'
        return context


class EventDetailView(DetailView):
    """Detail view of an event"""
    model = Event
