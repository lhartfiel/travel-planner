from django.db import models
# from travel_users.models import CustomUser
from djrichtextfield.models import RichTextField


class TravelGroup(models.Model):
    travelers = models.ManyToManyField('travel_users.CustomUser', related_name='TravelGroup')
    trip_name = models.CharField(max_length=200, blank=False)

    def travel_group(self):
        group = self.objects.all()
        return group

    def __str__(self):
        return self.trip_name


class SightseeingIdeas(models.Model):
    sightseeing_idea = RichTextField(blank=True)
    travel_group = models.ForeignKey('TravelGroup', related_name='travel', on_delete=models.CASCADE)

    def sightseeing_ideas(self):
        test = self.objects.all()
        return test

    class Meta:
        verbose_name = 'Sightseeing Idea'

    def __str__(self):
        return self.sightseeing_idea


class RestaurantIdeas(models.Model):
    restaurant_idea = RichTextField(blank=True)
    travel_group = models.ForeignKey('TravelGroup', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Restaurant Idea'

    def __str__(self):
        return self.restaurant_idea


class TravelMessages(models.Model):
    message = RichTextField(blank=True)
    travel_group = models.ForeignKey('TravelGroup', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Travel Message'

    def __str__(self):
        return self.message


