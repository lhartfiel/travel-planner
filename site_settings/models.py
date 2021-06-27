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

    def get_random_photo(self, search_term):
        hero = f'https://api.unsplash.com/search/photos?client_id' \
               f'=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM&query={search_term}&page=1'
        response = requests.get(hero)
        response = response.json()
        return response

    def save(self, *args, **kwargs):
        search_terms = [{'accommodation_photo': 'hotel room switzerland'}, \
                        {'travelgroup_photo': 'nordegg_lake_mountain_kayak'}, \
                        {'transportation_photo': 'aircraft sunset glider'}, \
                        {'profile_photo': 'relaxation zen beach pebble'}, \
                        {'checklist_photo': 'travel packing'}, \
                        {'sightseeing_photo': 'tour bus'}, \
                        {'restaurant_photo': 'outdoor cafe europe'}]
        photos_ids = ['AH8zKXqFITA', 'kGSapVfg8Kw', 'YvCg5X3pWzc', 'KBn4-lyqRgQ', 'TVllFyGaLEA', '8w_REsWW9Xw',
                      'bOICdD-Gulk']

        for idx, id in enumerate(photos_ids):
            hero = f'https://api.unsplash.com/photos/{id}?client_id' \
                   f'=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM'
            response = requests.get(hero)
            response = response.json()
            if response.get('urls'):
                if idx == 0:
                    self.accommodation_photo = response["urls"]["regular"]
                    self.accommodation_photo_attribution = response["user"]["name"]
                if idx == 1:
                    self.travelgroup_photo = response["urls"]["regular"]
                    self.travelgroup_photo_attribution = response["user"]["name"]
                if idx == 2:
                    self.transportation_photo = response["urls"]["regular"]
                    self.transportation_photo_attribution = response["user"]["name"]
                if idx == 3:
                    self.profile_photo = response["urls"]["regular"]
                    self.profile_photo_attribution = response["user"]["name"]
                if idx == 4:
                    self.checklist_photo = response["urls"]["regular"]
                    self.checklist_photo_attribution = response["user"]["name"]
                if idx == 5:
                    self.sightseeing_photo = response["urls"]["regular"]
                    self.sightseeing_photo_attribution = response["user"]["name"]
                if idx == 6:
                    self.restaurant_photo = response["urls"]["regular"]
                    self.restaurant_photo_attribution = response["user"]["name"]

        # If the above photos have been deleted or the Ids have changed in Unsplash, this will select the first random
        # photo from the given search term
        for element in search_terms:
            for key in element:
                value = element.get(key)
                if len(self.__getattribute__(key)) == 0:
                    response = self.get_random_photo(value)
                    self.__setattr__(key, response['results'][0]["urls"]["regular"])
                    self.__setattr__(f'{key}_attribution', response['results'][0]["user"]["name"])

        super(SiteSettings, self).save(*args, **kwargs)
