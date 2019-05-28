# travel_users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserEditForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'city', 'state', 'profile_photo', 'phone', 'emergency_first_name', 'emergency_last_name', 'emergency_email', 'emergency_phone', 'allergies', 'notes']
