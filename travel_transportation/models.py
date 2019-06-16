from django.db import models
from datetime import datetime


class Transportation(models.Model):
    arrival_date = models.DateField( blank=True)
    arrival_city = models.CharField(max_length=200, blank=True)
    arrival_time = models.TimeField(blank=True)
    departure_date = models.DateField(blank=True)
    departure_city = models.CharField(max_length=200, blank=True)
    departure_time = models.TimeField(blank=True)
    flight_no = models.IntegerField(blank=True)
    name = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    type = models.CharField(max_length=200, blank=True, help_text='Enter the type (flight, car, Eurail)')
    user = models.ForeignKey('travel_users.CustomUser', related_name='user_transport', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
