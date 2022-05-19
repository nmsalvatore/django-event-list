from django.contrib import admin
from .models import Event, ScraperEvent

# Register your models here.
admin.site.register(Event)
admin.site.register(ScraperEvent)