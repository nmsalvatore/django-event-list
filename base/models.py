from django.db import models

# Create your models here.
class Event(models.Model):
    class Meta:
        ordering = ['date']

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateTimeField(null=True)
    end_time = models.TimeField(null=True, blank=True)
    cost = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
