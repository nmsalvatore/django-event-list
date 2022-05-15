from django import forms

class DatePicker(forms.DateTimeInput):
    input_type = 'datetime-local'

class TimePicker(forms.TimeInput):
    input_type = 'time'