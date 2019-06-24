from django.db import models
# from travel_users.models import CustomUser
from djrichtextfield.models import RichTextField
from travel_transportation.models import Transportation


class TravelGroup(models.Model):
    transportation = models.ForeignKey(Transportation, related_name='transportation', on_delete=models.SET_NULL,
                                       null=True, blank=True)
    travelers = models.ManyToManyField('travel_users.CustomUser', related_name='TravelGroup')
    trip_name = models.CharField(max_length=200, blank=False)

    def travel_group(self):
        group = self.objects.all()
        return group

    def __str__(self):
        return self.trip_name


class SightseeingIdeas(models.Model):
    sightseeing_idea = RichTextField(blank=True)
    travel_group = models.ForeignKey('TravelGroup', related_name='sightseeing_ideas', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Sightseeing Idea'

    def __str__(self):
        return self.sightseeing_idea


class RestaurantIdeas(models.Model):
    restaurant_idea = RichTextField(blank=True)
    travel_group = models.ForeignKey('TravelGroup', related_name='restaurant_ideas', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Restaurant Idea'

    def __str__(self):
        return self.restaurant_idea


class TravelMessages(models.Model):
    message = RichTextField(blank=True)
    travel_group = models.ForeignKey('TravelGroup', related_name='messages', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Travel Message'

    def __str__(self):
        return self.message

