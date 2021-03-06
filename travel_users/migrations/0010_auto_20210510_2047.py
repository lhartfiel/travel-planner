# Generated by Django 3.0.4 on 2021-05-11 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_users', '0009_auto_20210411_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to='media/photos/%Y'),
        ),
    ]
