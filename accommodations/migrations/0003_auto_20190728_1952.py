# Generated by Django 2.2.1 on 2019-07-29 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0002_accommodations_trip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accommodations',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='accommodations',
            name='trip',
            field=models.ForeignKey(limit_choices_to={'travelers': True}, on_delete=django.db.models.deletion.CASCADE, related_name='user_trip', to='travel_group.TravelGroup'),
        ),
        migrations.AlterField(
            model_name='accommodations',
            name='user',
            field=models.ForeignKey(default=1, limit_choices_to={'id': True}, on_delete=django.db.models.deletion.CASCADE, related_name='user_accommodation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accommodations',
            name='zip',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
