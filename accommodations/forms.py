from django.forms import ModelForm
from . models import Accommodations
from travel_transportation.forms import DateInputWidget


class AccommodationEditForm(ModelForm):

    class Meta:
        model = Accommodations
        fields = '__all__'
        widgets = {'date_check_in': DateInputWidget(), 'date_check_out': DateInputWidget()}


class AccommodationCreateForm(ModelForm):

    class Meta:
        model = Accommodations
        fields = '__all__'
        widgets = {'date_check_in': DateInputWidget(), 'date_check_out': DateInputWidget()}