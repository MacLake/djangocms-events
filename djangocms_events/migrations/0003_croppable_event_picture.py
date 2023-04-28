# Generated by Django 3.2.18 on 2023-04-24 15:03

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import djangocms_events.models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('djangocms_events', '0002_calendar_default_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('picture', '852x426', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
        migrations.AlterField(
            model_name='event',
            name='picture',
            field=djangocms_events.models.CroppableFilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_picture', to=settings.FILER_IMAGE_MODEL, verbose_name='picture'),
        ),
    ]
