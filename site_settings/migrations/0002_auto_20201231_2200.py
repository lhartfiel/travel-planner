# Generated by Django 3.0.4 on 2021-01-01 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='checklist_photo',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='checklist_photo_attribution',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
    ]
