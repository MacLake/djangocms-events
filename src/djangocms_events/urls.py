from typing import Any

import arrow
from django.urls import path

from . import views

app_name: str = 'djangocms_events'
urlpatterns: list[Any] = [
    path('import_calendars', views.import_calendars, name='import_calendars'),
    path(
        'import_calendars_future_events',
        views.import_calendars, {'start_after_date': arrow.utcnow()},
        name='import_calendars'
    ),
    path('', views.FutureEventListView.as_view(), name='future_event_list'),
    path('past', views.PastEventListView.as_view(), name='past_event_list'),
    path('all', views.EventListView.as_view(), name='event_list'),
    path(
        'event/<int:pk>', views.EventDetailView.as_view(), name='event_detail'
    ),
]
