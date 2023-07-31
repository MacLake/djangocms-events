from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class EventsApphook(CMSApp):
    app_name: str = "djangocms_events"
    name: str = "Events"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["djangocms_events.urls"]
