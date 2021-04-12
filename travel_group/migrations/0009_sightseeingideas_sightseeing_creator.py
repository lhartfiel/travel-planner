# Generated by Django 3.0.4 on 2020-04-13 02:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel_group', '0008_checklistitems_item_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sightseeingideas',
            name='sightseeing_creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sightseeing_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]