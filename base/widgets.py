from django import forms

class DatePicker(forms.DateInput):
    input_type = 'date'

class TimePicker(forms.TimeInput):
    input_type = 'time'