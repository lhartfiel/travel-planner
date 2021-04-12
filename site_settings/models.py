import requests
from django.db import models

from django.contrib.sites.models import Site


class SiteSettings(models.Model):
    accommodation_photo = models.CharField(max_length=600, blank=True, default="")
    accommodation_photo_attribution = models.CharField(max_length=600, blank=True, default="")
    checklist_photo = models.CharField(max_length=600, blank=True, default="")
    checklist_photo_attribution = models.CharField(max_length=600, blank=True, default="")
    profile_photo = models.CharField(max_length=600, blank=True, default="")
    profile_photo_attribution = models.CharField(max_length=600, blank=True, default="")
    restaurant_photo = models.CharField(max_length=600, blank=True, default="")
    restaurant_photo_attribution = models.CharField(max_length=600, blank=True, default="")
    sightseeing_photo = models.CharField(max_length=600, blank=True, default="")
    sightseeing_photo_attribution = models.CharField(max_length=600, blank=True, default="")
    transportation_photo = models.CharField(max_length=600, blank=True, default="")
    transportation_photo_attribution = models.CharField(max_length=600, blank=True, default="")
    travelgroup_photo = models.CharField(max_length=600, blank=True, default="")
    travelgroup_photo_attribution = models.CharField(max_length=600, blank=True, default="")

    def __str__(self):
        return 'site settings'

    def save(self, *args, **kwargs):
        search_terms = ['hotel room switzerland', 'nordegg_lake_mountain_kayak', 'aircraft sunset glider',
                        'relaxation zen beach pebble', 'travel packing', 'tour bus', 'outdoor cafe europe']
        for idx, term in enumerate(search_terms):
            hero = f'https://api.unsplash.com/search/photos?client_id' \
                               f'=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM&query={term}&page=1'
            response = requests.get(hero)
            response = response.json()
            if idx == 0:
                self.accommodation_photo = response['results'][4]["urls"]["regular"]
                self.accommodation_photo_attribution = response['results'][4]["user"]["name"]
            elif idx == 1:
                self.travelgroup_photo = response['results'][0]["urls"]["regular"]
                self.travelgroup_photo_attribution = response['results'][0]["user"]["name"]
            elif idx == 2:
                self.transportation_photo = response['results'][6]["urls"]["regular"]
                self.transportation_photo_attribution = response['results'][6]["user"]["name"]
            elif idx == 3:
                self.profile_photo = response['results'][0]["urls"]["regular"]
                self.profile_photo_attribution = response['results'][0]["user"]["name"]
            elif idx == 4:
                self.checklist_photo = response['results'][2]["urls"]["regular"]
                self.checklist_photo_attribution = response['results'][2]["user"]["name"]
            elif idx == 5:
                self.sightseeing_photo = response['results'][2]["urls"]["regular"]
                self.sightseeing_photo_attribution = response['results'][2]["user"]["name"]
            elif idx == 6:
                self.restaurant_photo = response['results'][4]["urls"]["regular"]
                self.restaurant_photo_attribution = response['results'][4]["user"]["name"]
        super(SiteSettings, self).save(*args, **kwargs)



