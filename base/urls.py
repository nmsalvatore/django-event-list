from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('add-event/', views.addEvent, name="add-event"),
    path('event/<int:pk>/', views.eventDetails, name="event-details"),
    path('update-event/<int:pk>/', views.updateEvent, name="update-event"),
    path('delete-event/<int:pk>/', views.deleteEvent, name="delete-event"),
    path('duplicate-event/<int:pk>/', views.duplicateEvent, name="duplicate-event"),
    path('scraper/', views.downloadScraperData, name="scraper")
]