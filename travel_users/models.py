from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, QuerySet
from phonenumber_field.modelfields import PhoneNumberField
from travel_group.models import TravelGroup
from travel_transportation.models import Transportation


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='photos/%Y', blank=True)
    phone = PhoneNumberField(blank=True)
    emergency_first_name = models.CharField(max_length=255, blank=True)
    emergency_last_name = models.CharField(max_length=255, blank=True)
    emergency_phone = PhoneNumberField(blank=True)
    emergency_email = models.EmailField(max_length=255, blank=False)
    allergies = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def get_profile(self):
        user = self.objects.all()
        return user

    def get_transport_id(self):
        return CustomUser.objects.get(id=self.transportation.id)

    def order_by_travel_group(self):
        return Transportation.objects.filter(user_id=self.id).order_by('travel_group')

    def __str__(self):
        return self.first_name

