from django.shortcuts import render, redirect
from datetime import datetime
from .models import Event
from .forms import EventForm

# Create your views here.
def home(request):
    today = datetime.now().date()
    events = Event.objects.all()
    event_dates = Event.objects.dates('date', 'day')
    context = {
        'today': today,
        'events': events,
        'event_dates': event_dates
    }
    return render(request, 'base/home.html', context)

def addEvent(request):
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)
        form.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'base/event-form-add.html', context)

def updateEvent(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        form.save()
        return redirect('home')

    context = {
        'form': form,
        'event': event
    }
    return render(request, 'base/event-form-edit.html', context)

def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)

    if request.method == 'POST':
        event.delete()
        return redirect('home')
        
    context = {'event': event}
    return render(request, 'base/event-delete.html', context)

def eventDetails(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}
    return render(request, 'base/event-details.html', context)