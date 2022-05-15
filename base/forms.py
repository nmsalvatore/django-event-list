from django import forms
from django.forms import ModelForm, Textarea
from .models import Event
from .widgets import DatePicker, TimePicker

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(attrs={'placeholder': 'Event Name'}),
            'location' : forms.TextInput(attrs={'placeholder': 'Location'}),
            'date': DatePicker(),
            'end_time': TimePicker(),
            'description' : Textarea(attrs={'placeholder': 'Description'}),
            'cost' : forms.TextInput(attrs={'placeholder': 'Price'}),
        }

    