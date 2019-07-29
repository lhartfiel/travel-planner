from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

# Create your models here.


class Accommodations(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=False)
    country = models.CharField(max_length=255, blank=False)
    date_check_in = models.DateTimeField()
    date_check_out = models.DateTimeField()
    name = models.CharField(max_length=255, blank=False)
    notes = models.TextField(blank=True)
    phone = PhoneNumberField(blank=True)
    trip = models.ForeignKey('travel_group.TravelGroup', related_name='user_trip', on_delete=models.CASCADE, limit_choices_to={'travelers': True},)
    type = models.CharField(max_length=255, help_text="AirBnB, Hotel, Hostel, etc")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_accommodation', on_delete=models.CASCADE, default=1, limit_choices_to={'id': True})
    zip = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

