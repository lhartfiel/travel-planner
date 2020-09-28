from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import render
from requests import Response

from travel_group.models import TravelGroup

import requests

from travel_group.views import TravelGroupImage


class Command(BaseCommand):
    help = 'Call the Unsplash API once per hour'

    def handle(self, *args, **options):
        photo_list = TravelGroup.objects.values_list('primary_destination', flat=True).distinct()
        filtered_list = list(filter(None, photo_list))
        photo_dict = dict()
        for photo in filtered_list:
            unsplash_api = f'https://api.unsplash.com/search/photos?client_id=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM&query={photo}&page=1'
            try:
                response = requests.get(unsplash_api)
                response = response.json()
                photo_url = response['results'][0]["urls"]["regular"]
                photographer_name = response['results'][0]["user"]["name"]
                photo_dict[f'{photo}'] = {'url': photo_url, 'photographer': photographer_name}
            except AttributeError:
                pass
        unsplash_data = {'results': photo_dict}
        # return Response(context)
        # return render(request, "travel_group/photo.html", context=context)