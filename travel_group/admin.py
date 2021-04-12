from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from travel_group.models import TravelGroup, SightseeingIdeas, RestaurantIdeas, TravelMessages, ChecklistItems, \
    UnsplashPhotos

import requests


class ChecklistItemsAdmin(admin.TabularInline):
    model = ChecklistItems
    fields = ('checklist_item', 'checklist_creator', 'item_status', 'travel_group',)
    extra = 1

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance


class UnsplashAdmin(admin.TabularInline):
    model = UnsplashPhotos
    fields = ('photo', 'photo_attribution',)
    extra = 1


class SightseeingIdeasAdmin(admin.TabularInline):
    model = SightseeingIdeas
    fields = ('sightseeing_idea',)
    extra = 1


class RestaurantIdeasAdmin(admin.TabularInline):
    model = RestaurantIdeas
    fields = ('restaurant_idea',)
    extra = 1


class TravelMessagesAdmin(admin.TabularInline):
    model = TravelMessages
    fields = ('message',)
    extra = 1

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance


class TravelGroupAdmin(admin.ModelAdmin):
    list_display = ('trip_name',)
    fieldsets = (
        (None, {
            'fields': ('trip_name', 'travelers', 'primary_destination', )
        }),
    )
    inlines = [
        UnsplashAdmin,
        SightseeingIdeasAdmin,
        RestaurantIdeasAdmin,
        TravelMessagesAdmin,
        ChecklistItemsAdmin,
    ]

    def call_unsplash_api(self, current_obj_id, request):
        current_group = TravelGroup.objects.get(id=current_obj_id)
        destination = current_group.primary_destination
        unsplash_api = f'https://api.unsplash.com/search/photos?client_id=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM' \
                       f'&query={destination}&page=1'
        photo_dict = {}
        try:
            response = requests.get(unsplash_api)
            response = response.json()
            photo_url = response['results'][0]["urls"]["regular"]
            photographer_name = response['results'][0]["user"]["name"]
            photo_dict = {'url': photo_url, 'photographer': photographer_name}
        except AttributeError:
            pass
        return photo_dict

    def save_model(self, request, obj, form, change):
        current_obj_id = request.resolver_match.kwargs['object_id']
        current_group = TravelGroup.objects.get(id=current_obj_id)
        try:
            UnsplashPhotos.objects.get(travel_group=current_obj_id)
        except ObjectDoesNotExist:
            unsplash_photo = self.call_unsplash_api(current_obj_id, request)
            photo = unsplash_photo['url']
            photo_attribute = unsplash_photo['photographer']
            new_photo = UnsplashPhotos(
                photo=photo,
                photo_attribution=photo_attribute,
                travel_group=current_group
            )
            new_photo.save(force_insert=True)
        super().save_model(request, obj, form, change)

admin.site.register(TravelGroup, TravelGroupAdmin)
