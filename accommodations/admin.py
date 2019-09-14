from django.contrib import admin
from .models import Accommodations

# Register your models here.


class AccommodationsAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'date_check_in', 'date_check_out', ]


admin.site.register(Accommodations, AccommodationsAdmin)
