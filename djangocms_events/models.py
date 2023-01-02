import json

import ics
import requests
from arrow import Arrow
from cms.models import CMSPlugin
from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField
from filer.fields.image import FilerImageField
from ics import Calendar as ICSCalendar
from ics.timeline import Timeline as ICSTimeline


class Calendar(models.Model):
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    name = models.CharField(max_length=50, verbose_name=_('name'))
    url = models.URLField(
        blank=True,
        verbose_name=_('URL of ics file'),
        help_text=_(
            'Calendar to be imported, leave empty if you edit events only here in the admin section.'
        )
    )
    ics = models.TextField(blank=True, verbose_name=_('imported ics file'))
    colour = models.CharField(
        blank=True, max_length=20, verbose_name=_('colour')
    )
    publish = models.BooleanField(default=True, verbose_name=_('publish'))

    class Meta:
        verbose_name = _('calendar')
        verbose_name_plural = _('calendars')

    def __str__(self):
        return self.name

    def import_ics(self, start_after_date: Arrow = None) -> None:
        """
        Import a calendar with a URL of an ics file with the ics lib
        and then create Django Event objects
        """
        calendar_ics: str = requests.get(self.url).text
        self.ics = calendar_ics  # Just for debugging
        self.save()

        ics_calendar: ICSCalendar = ICSCalendar(calendar_ics)
        ics_timeline: ICSTimeline = ics_calendar.timeline.start_after(
            start_after_date
        ) if start_after_date else ics_calendar.timeline
        ics_event: ics.Event
        for ics_event in ics_timeline:
            event: Event
            event, _ = Event.objects.get_or_create(
                calendar=self, uid=ics_event.uid
            )
            # QuillField can’t be set directly, code taken from
            # https://github.com/LeeHanYeong/django-quill-editor/blob/master/django_quill/management/commands/convert_to_quill.py#L48
            description_json: str = json.dumps(
                {
                    'delta': '',
                    'html': ics_event.description
                }
            )
            event.name = ics_event.name
            event.begin = ics_event.begin.datetime
            event.end = ics_event.end.datetime
            event.duration = ics_event.duration
            event.description = description_json
            event.created = ics_event.created.datetime
            event.last_modified = ics_event.last_modified.datetime
            event.location = ics_event.location
            event.url = ics_event.url
            event.transparent = ics_event.transparent
            event.status = ics_event.status
            event.organizer = ics_event.organizer
            event.classification = ics_event.classification
            event.save()


class Event(models.Model):
    calendar = models.ForeignKey(
        Calendar, on_delete=models.CASCADE, verbose_name=_('calendar')
    )
    name = models.CharField(blank=True, max_length=255, verbose_name=_('name'))
    begin = models.DateTimeField(null=True, blank=True, verbose_name=_('begin'))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_('end'))
    # TODO: Check if django-timedeltafield is worth being installed:
    duration = models.CharField(
        null=True, blank=True, max_length=64, verbose_name=_('duration')
    )
    uid = models.CharField(
        null=True, blank=True, max_length=255, verbose_name=_('uid')
    )
    description = QuillField(blank=True, verbose_name=_('description'))
    created = models.DateTimeField(
        null=True, blank=True, verbose_name=_('created')
    )
    last_modified = models.DateTimeField(
        null=True, blank=True, verbose_name=_('last_modified')
    )
    location = models.CharField(
        null=True, blank=True, max_length=255, verbose_name=_('location')
    )
    url = models.URLField(null=True, blank=True, verbose_name=_('url'))
    transparent = models.BooleanField(
        null=True, blank=True, verbose_name=_('transparent')
    )
    # alarms (Optional[Iterable[BaseAlarm]])
    # attendees (Optional[Iterable[Attendee]])
    # categories (Optional[Iterable[str]])
    status = models.CharField(
        null=True, blank=True, max_length=64, verbose_name=_('status')
    )
    organizer = models.CharField(
        null=True, blank=True, max_length=255, verbose_name=_('organizer')
    )
    classification = models.CharField(
        null=True, blank=True, max_length=64, verbose_name=_('classification')
    )
    picture = FilerImageField(
        null=True,
        blank=True,
        verbose_name=_('picture'),
        related_name='event_picture',
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'{self.begin} {self.name}'

    class Meta:
        verbose_name: str = _('event')
        verbose_name_plural: str = _('events')
        unique_together = ['calendar', 'uid']
        ordering: list[str] = ['-begin', '-end']

    @property
    def one_day(self):
        return self.begin.date() == self.end.date()


class EventCalendarPlugin(CMSPlugin):
    calendars = models.ManyToManyField(Calendar, verbose_name=_('calendars'))

    class Meta:
        abstract: bool = True

    def copy_relations(self, oldinstance):
        self.calendars.set(oldinstance.calendars.all())


class EventListPlugin(EventCalendarPlugin):
    number = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=5,
        verbose_name=_('number of events'),
        help_text=_('Number of events to be displayed, unlimited if empty')
    )
    also_past_events = models.BooleanField(
        default=False,
        verbose_name=_('also past events'),
        help_text=_(
            'If the number of future events is smaller than the chosen number, also '
            'show past events.'
        )
    )

    def __str__(self) -> str:
        return f'{self.number if self.number else "all"} events'


class CalendarPlugin(EventCalendarPlugin):
    height = models.PositiveSmallIntegerField(
        default=800, verbose_name=_('height in px')
    )
    CALENDAR_VIEWS = [
        ('month', _('month')), ('week', _('week')), ('day', _('day'))
    ]
    default_view = models.CharField(
        max_length=5,
        choices=CALENDAR_VIEWS,
        default='month',
        verbose_name=_('default view')
    )

    def __str__(self) -> str:
        return 'Calendar'
