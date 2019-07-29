from django.forms import ModelForm
from . models import Accommodations


class AccommodationEditForm(ModelForm):

    class Meta:
        model = Accommodations
        fields = '__all__'