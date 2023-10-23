from django.contrib.sitemaps import Sitemap
from django.db.models import QuerySet

from .models import Event


class EventSitemap(Sitemap):
    priority: float = 0.5

    def items(self) -> QuerySet:
        return Event.objects.all()

    def lastmod(self, obj):
        return obj.last_modified
