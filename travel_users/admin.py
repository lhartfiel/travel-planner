from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomerUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'city']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username', 'city', 'state', 'profile_photo', 'phone', 'allergies')}),
        ('Emergency Info', {'fields': ('emergency_first_name', 'emergency_last_name', 'emergency_phone', 'emergency_email')}),
        ('Additional Notes', {'fields': ('notes',)})
    )


admin.site.register(CustomUser, CustomerUserAdmin)
