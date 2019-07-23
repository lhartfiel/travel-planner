from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Accommodations(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=False)
    country = models.CharField(max_length=255, blank=False)
    date_check_in = models.DateTimeField()
    date_check_out = models.DateTimeField()
    name = models.CharField(max_length=255, blank=False)
    notes = models.TextField(blank=True)
    phone = PhoneNumberField()
    type = models.CharField(max_length=255, help_text="AirBnB, Hotel, Hostel, etc")
    user = models.ForeignKey('travel_users.CustomUser', related_name='user_accommodation', on_delete=models.CASCADE)
    zip = models.CharField(max_length=255)

    def __str__(self):
        return self.name

