# Generated by Django 2.2.1 on 2019-06-15 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transportation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_date', models.DateField(blank=True)),
                ('arrival_city', models.CharField(blank=True, max_length=200)),
                ('arrival_time', models.TimeField(blank=True)),
                ('departure_date', models.DateField(blank=True)),
                ('departure_city', models.CharField(blank=True, max_length=200)),
                ('departure_time', models.TimeField(blank=True)),
                ('flight_no', models.IntegerField(blank=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('notes', models.TextField(blank=True)),
                ('type', models.CharField(blank=True, help_text='Enter the type (flight, car, Eurail)', max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_transport', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]