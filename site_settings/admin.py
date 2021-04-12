from django.contrib import admin

# Register your models here.
from site_settings.models import SiteSettings


class SiteSettingsAdmin(admin.ModelAdmin):
    fields = ['accommodation_photo', 'accommodation_photo_attribution', 'checklist_photo',
              'checklist_photo_attribution', 'profile_photo', 'profile_photo_attribution',
              'transportation_photo', 'transportation_photo_attribution', 'travelgroup_photo', 'travelgroup_photo_attribution']
    list_display = ('accommodation_photo', 'accommodation_photo_attribution', 'checklist_photo',
              'checklist_photo_attribution', 'profile_photo', 'profile_photo_attribution',
              'transportation_photo', 'transportation_photo_attribution', 'travelgroup_photo', 'travelgroup_photo_attribution')
    model = SiteSettings


admin.site.register(SiteSettings, SiteSettingsAdmin)


