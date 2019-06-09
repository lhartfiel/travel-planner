from django.contrib import admin
from travel_group.models import TravelGroup, SightseeingIdeas, RestaurantIdeas, TravelMessages

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


class TravelGroupAdmin(admin.ModelAdmin):
    list_display = ('trip_name',)
    fieldsets = (
        (None, {
            'fields': ('trip_name', 'travelers')
        }),
    )
    inlines = [
        SightseeingIdeasAdmin,
        RestaurantIdeasAdmin,
        TravelMessagesAdmin
    ]


admin.site.register(TravelGroup, TravelGroupAdmin)
