from django.contrib import admin
from .models import Transportation


class TransportationAdmin(admin.ModelAdmin):
    list_display = ['name', 'departure_city', 'arrival_city',]


admin.site.register(Transportation, TransportationAdmin)