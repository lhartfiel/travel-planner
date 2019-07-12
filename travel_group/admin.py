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
            'fields': ('trip_name', 'travelers')
        }),
    )
    inlines = [
        SightseeingIdeasAdmin,
        RestaurantIdeasAdmin,
        TravelMessagesAdmin
    ]


admin.site.register(TravelGroup, TravelGroupAdmin)
