from django.shortcuts import render, redirect
from datetime import datetime
from .models import Event, ScraperEvent
from .forms import EventForm
from .scraper import get_all_scraper_events

# Create your views here.
def home(request):
    return redirect('by-date')

def listByDate(request):
    today = datetime.now().date()
    events = Event.objects.all().order_by('date', 'start_time')
    event_dates = Event.objects.dates('date', 'day')
    context = {
        'today': today,
        'events': events,
        'event_dates': event_dates
    }
    return render(request, 'base/list-by-date.html', context)

def addEvent(request):
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)
        print(request.POST)
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

def duplicateEvent(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)

    if request.method == 'POST':
        form = EventForm(request.POST)
        form.save()
        return redirect('event-details', pk=pk)

    context = {
        'form': form,
        'event': event
    }
    return render(request, 'base/event-form-add.html', context)

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

def downloadScraperData(request):
    context = {}
    
    if request.method == 'POST':
        event_data = get_all_scraper_events()
        events = event_data['events']
        skipped = event_data['skipped']
        added = []

        count = 0
        
        for event in events:
            duplicate = Event.objects.filter(
                title=event['title'], 
                date=event['date'],
                start_time=event['start_time']
            )
            
            if duplicate:
                continue

            try: end_time = event['end_time']
            except: end_time = None

            try: cost = event['cost']
            except: cost = None

            try: description = event['description']
            except: description = None
            
            new_event = Event.objects.create(
                title=event['title'],
                location=event['location'],
                date=event['date'],
                start_time=event['start_time'],
                end_time=end_time,
                cost=cost,
                description=description
            )

            count = count + 1
            added.append(event)
        
        added = sorted(added, key=lambda x:x['date'])
        context = {
            'events_added': added,
            'events_count': count,
            'events_skipped': skipped,
        }

    return render(request, 'base/scraper.html', context)

def listByVenue(request):
    today = datetime.now().date()
    events = Event.objects.all().order_by('date', 'start_time')
    venues = Event.objects.values_list('location', flat=True)
    venues = set(venues)
    venues = sorted(venues)

    context = {
        'venues': venues,
        'events': events,
        'today': today
    }

    return render(request, 'base/list-by-venue.html', context)