# djangocms-events

Events and calendar with ics import for django CMS

## Installation, required libraries and settings

Currently you can install this package with

```python
pip install git+https://github.com/MacLake/djangocms-events.git
```
or add
```
djangocms-events @ git+https://github.com/MacLake/djangocms-events.git
```
to your requirements. A pip package will be available soon. 


### Python packages

This package uses sekizai, which is required by django CMS anyway.

The description of events can be formatted text and is saved in a QuillField,
so [django-quill-editor](https://pypi.org/project/django-quill-editor/) is required.

In the templates for event lists and detail
view [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails) is used. This requires
an entry in INSTALLED_APPS in your project settings:

```python
INSTALLED_APPS: list[str] = [
    ...
    'sekizai',
    'easy_thumbnails',
    'django_quill',
    'djangocms_events',
]
```

and a definition for the thumbnail sizes:

```python
THUMBNAIL_ALIASES: dict[str, dict[str, dict[str, any]]] = {
    '':
        {
            'event-list': {
                'size': (600, 300),
                'crop': True,
                'upscale': True
            },
            'event-detail': {
                'size': (600, 300),
                'crop': False,
                'upscale': True
            },
        }
}
```

The following settings are optional:

```python
DJANGOCMS_EVENTS_SHOW_CALENDAR_MONTH_WEEK_DAY_CONTROL: bool = False
DJANGOCMS_EVENTS_PAGINATE_BY: int = 100
DJANGOCMS_EVENTS_NR_INITIALLY_SHOWN: int = 5

```

With `DJANGOCMS_EVENTS_SHOW_CALENDAR_MONTH_WEEK_DAY_CONTROL` you can choose if the control for
switching between month, week and day view in the calendar is shwon or hidden. If it’s not set, it
will be shown. `DJANGOCMS_EVENTS_PAGINATE_BY` sets the number of events per page in the events list
and defaults to 100. With setting `DJANGOCMS_EVENTS_NR_INITIALLY_SHOWN` to a number that is smaller
than the number of events per page, only this number of events will be shown on the overview, the
rest will be hidden in an accordion, otherwise no events will be hidden.

### JavaScript frontend libraries

The frontend uses the framework Fomantic UI in general and especially for modal overlays and
optionally an accordion. In its current version it needs jQuery which is also used for event
handling. Ajax requests for getting the content of event details are done with htmx. These libraries
are included in the webpack bundle
`djangocms_events/static/djangocms_events/webpack/index.bundle.js`. In case you already have one or
more of these libraries in your CMS base template, so that you don’t need this bundle, or you want
to adopt the templates to integrate it into your website, you can override the templates by copying
them to your project and modify them. You might want to build your own webpack bundle based
on `assets/src/index.js`. If you do, you should rename index in `entry` in `webpack.config.js` in
order to avoid a name conflict with the shipped bundle and link your own bundle.

Short instruction for building the webpack bundles: Clone this repo and enter it in a shell.

```shell
npm install
npx webpack
```

The second bundle `djangocms_events/static/djangocms_events/webpack/calendar.bundle.js is used for
the calendar view in the apphook page and the calendar plug-in.

## Usage
After installing and configuring the package you can integrate it in django CMS as a webhook page in
the advanced settings of a CMS page.

You can edit events in the Django admin or import an ICS file. In either case first create a
calendar in the admin. If you want to import an ICS file available in the Internet, enter its URL,
otherwise leave this field empty. You can import events after having checked the “publish” field in 
the calendar by applying an admin action or by calling a URL for importing the events e.g. in a
cron job. The URL for importing all events of all published calendars is the URL of your apphook
page plus `import_calendars` or `import_calendars_future_events` for just importing events in the
future.

On the apphook page you can see a calendar and a list of the events. The default view shows only
events of the current and future months in the calendar and future events in the list, because
calendars with thousands of events in the past take much more time to render, even with pagination.
With a menu you can also go to pages with the past or all events.

In addition, there are plug-ins for event lists and calendar views. You can choose which calendars,
i.e. groups of events will be shown. In the event list plug-in you can choose how many events
are being shown, and if there are not enough future events, you can choose to fill up the list with
recent events, so the list won’t look too empty in that case.


## Integrated libraries

| Name                                                   | Used for                               | License                                                                            |
|--------------------------------------------------------|----------------------------------------|------------------------------------------------------------------------------------|
| [jquery](https://jquery.com/)                          | Needed for Fomantic UI, event handling | [MIT license](https://github.com/jquery/jquery/blob/main/LICENSE.txt)              |
| [Fomantic UI](https://fomantic-ui.com/ )               | frontend library                       | [MIT license](https://github.com/jquery/jquery/blob/main/LICENSE.txt)              
| [htmx](https://htmx.org/)                              | Ajax requests for detail views         | [BSD-2-Clause license](https://github.com/bigskysoftware/htmx/blob/master/LICENSE) 
| [Toast UI Calendar](https://ui.toast.com/tui-calendar) | JS calendar                            | [MIT License](https://github.com/nhn/tui.calendar/blob/main/LICENSE)               

