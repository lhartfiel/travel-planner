# Generated by Django 3.0.4 on 2020-08-31 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel_group', '0013_travelgroup_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='unsplashphotos',
            name='photo_attribution',
            field=models.CharField(blank=True, max_length=600),
        ),
        migrations.AddField(
            model_name='unsplashphotos',
            name='travel_group',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='unsplash_photo', to='travel_group.TravelGroup'),
            preserve_default=False,
        ),
    ]
