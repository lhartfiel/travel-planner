from datetime import datetime

from django.db import models
# from travel_users.models import CustomUser
from djrichtextfield.models import RichTextField

from accommodations.models import Accommodations
from travel_transportation.models import Transportation


class UnsplashPhotos(models.Model):
    photo = models.CharField(max_length=400, blank=True)
    photo_attribution = models.CharField(max_length=600, blank=True)
    travel_group = models.ForeignKey('TravelGroup', related_name='unsplash_photo', on_delete=models.CASCADE)

    def __str__(self):
        return self.photo


class TravelGroup(models.Model):
    accommodations = models.ForeignKey(Accommodations, related_name='accommodation', on_delete=models.SET_NULL, null=True, blank=True)
    # photo = models.ForeignKey(UnsplashPhotos, related_name='display_photo', on_delete=models.SET_NULL, null=True,
    #                           blank=True)
    primary_destination = models.CharField(max_length=200, null=False, blank=False, default='')
    transportation = models.ForeignKey(Transportation, related_name='transportation', on_delete=models.SET_NULL,
                                       null=True, blank=True)
    travelers = models.ManyToManyField('travel_users.CustomUser', related_name='trav_groups', null=True, blank=True)
    group_owner = models.ForeignKey('travel_users.CustomUser', related_name='travel_group_owner', default=1,
                                    null=True, blank=False, on_delete=models.SET_NULL)
    trip_name = models.CharField(max_length=200, blank=False)

    def travel_group(self):
        group = self.objects.all()
        return group

    def get_context_data(self, **kwargs):
        context = super.get_context_data(**kwargs)

    def __str__(self):
        return self.trip_name


class ChecklistItems(models.Model):
    checklist_item = RichTextField(blank=True)
    checklist_creator = models.ForeignKey('travel_users.CustomUser', related_name='checklist_creator', on_delete=models.CASCADE)
    item_status = models.BooleanField(default=False)
    travel_group = models.ForeignKey('TravelGroup', related_name='checklist_items', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Checklist Items'

    def __str__(self):
        return self.checklist_item


class SightseeingIdeas(models.Model):
    sightseeing_idea = RichTextField(blank=True)
    sightseeing_creator = models.ForeignKey('travel_users.CustomUser', related_name='sightseeing_creator',
                                            on_delete=models.CASCADE, default=1)
    travel_group = models.ForeignKey('TravelGroup', related_name='sightseeing_ideas', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Sightseeing Idea'

    def __str__(self):
        return self.sightseeing_idea


class RestaurantIdeas(models.Model):
    restaurant_idea = RichTextField(blank=True)
    restaurant_creator = models.ForeignKey('travel_users.CustomUser', related_name='restaurant_creator',
                                            on_delete=models.CASCADE, default=1)
    travel_group = models.ForeignKey('TravelGroup', related_name='restaurant_ideas', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Restaurant Idea'

    def __str__(self):
        return self.restaurant_idea


class TravelMessages(models.Model):
    date_created_at = models.DateTimeField(default=datetime.now)
    date_updated_at = models.DateTimeField(default=datetime.now)
    message = RichTextField(blank=True)
    travel_group = models.ForeignKey('TravelGroup', related_name='messages', on_delete=models.CASCADE)
    message_creator = models.ForeignKey('travel_users.CustomUser', related_name='message_creator', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Travel Message'

    def __str__(self):
        return self.message


# class TravelGroupInvite(models.Model):
#     invitation = get_invitation_model()
#     recipient_email = models.EmailField(null=False, blank=False)
#     subject_line = models.CharField(max_length=300, blank=True, default="Join my travel group on Travel Planner")
#     travel_group = models.ForeignKey('TravelGroup', related_name='travel_group_invite', on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Travel Group Invite'
#
#     def __str__(self):
#         return self.travel_group
