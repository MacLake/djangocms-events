# Generated by Django 4.2.7 on 2023-11-13 15:15
import re
from datetime import timedelta

from django.db import migrations, models


def forwards(apps, schema_editor):
    Event = apps.get_model("djangocms_events", "Event")
    event: Event
    for event in Event.objects.all():
        if event.duration_str:
            # https://stackoverflow.com/questions/37611678/python-convert-str-to-timedelta
            days, hours, minutes, seconds = re.match(
                r'(?:(\d+) days?, )?(\d+):(\d+):([.\d+]+)', event.duration_str
            ).groups()
            total_seconds = (
                (int(days or 0) * 24 + int(hours)) * 60 + int(minutes)
            ) * 60 + float(seconds)
            event.duration = timedelta(seconds=total_seconds)
        else:
            event.duration = None
        event.save()


def backwards(apps, schema_editor):
    Event = apps.get_model("djangocms_events", "Event")
    event: Event
    for event in Event.objects.all():
        event.duration_str = str(event.duration or '')
        event.save()


class Migration(migrations.Migration):
    dependencies = [
        (
            "djangocms_events",
            "0003_alter_calendarplugin_cmsplugin_ptr_and_more"
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="duration",
            new_name="duration_str",
        ),
        migrations.AddField(
            model_name="event",
            name="duration",
            field=models.DurationField(
                blank=True, null=True, verbose_name="duration"
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name="event",
            name="duration_str",
        ),
    ]
