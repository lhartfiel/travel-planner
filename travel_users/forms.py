from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms import ModelForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists -- please select a different username.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address belongs to an existing user.")
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'city', 'state', 'profile_photo', 'phone', 'email', 'emergency_first_name',
                  'emergency_last_name', 'emergency_email', 'emergency_phone', 'allergies', 'notes']


class CustomUserEditForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'city', 'state', 'profile_photo', 'phone', 'email', 'emergency_first_name', 'emergency_last_name', 'emergency_email', 'emergency_phone', 'allergies', 'notes']
