# Generated by Django 2.2.1 on 2019-09-05 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0003_auto_20190728_1952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accommodations',
            old_name='name',
            new_name='title',
        ),
    ]
