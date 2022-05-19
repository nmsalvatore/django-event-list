import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, time
from urllib.request import Request, urlopen
# from .utils import convert_time

def convert_time(time_str):
    time_str = time_str.split(' ')
    hour = int(time_str[0].split(':')[0])

    if time_str[-1] == 'pm' or hour == 12 and time_str[-1] == 'am':
        hour = hour + 12

    if hour == 24:
        hour = 0

    minute = int(time_str[0].split(':')[1])
    return time(hour=hour, minute=minute).isoformat(timespec='minutes')

def convert_date(date_str):
    current_date = datetime.now().date()
    new_date = datetime.strptime(date_str, '%A, %B %d').date()

    if new_date.month >= current_date.month:
        new_date = new_date.replace(year=current_date.year)
    else:
        new_date = new_date.replace(year=current_date.year+1)
    
    return new_date

def get_miners_foundry_event_links():
    r = requests.get('https://minersfoundry.org/events/')
    soup = BeautifulSoup(r.content, 'html.parser')
    events = soup.find_all('div', 'tribe-events-pro-photo__event-details-wrapper')
    links = []

    for event in events:
        links.append(event.a.get('href'))

    return links

def get_miners_foundry_data():
    links = get_miners_foundry_event_links()
    data = []
    
    for link in links:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        times = soup.find(class_="tribe-events-start-time").get_text().split(' - ')
        start_time = convert_time(times[0].strip())
        end_time = convert_time(times[1].strip())
        iso_date = soup.find(class_="dtstart").get('title')

        event_details = {}
        event_details['title'] = soup.find(class_="entry-title").get_text()
        event_details['location'] = soup.find(class_="tribe-venue").a.get_text()
        event_details['date'] = date.fromisoformat(iso_date)
        event_details['start_time'] = start_time
        event_details['end_time'] = end_time
        event_details['cost'] = soup.find(class_="tribe-events-event-cost").get_text().strip()
        
        data.append(event_details)

    return data

def get_center_for_the_arts_data():
    url = 'https://thecenterforthearts.org/events/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    site_content = urlopen(req).read()
    soup = BeautifulSoup(site_content, 'html.parser')
    events = soup.find_all('div', 'event-cnt')
    data = []

    for event in events:
        date_str = event.find(class_='d').get_text().strip()
        event_details = {}
        event_details['title'] = event.h2.get_text()
        event_details['location'] = 'The Center For The Arts'
        event_details['date'] = datetime.strptime(date_str, '%b %d, %Y')
        event_details['start_time'] = event.find(class_='t').get_text().split(',')[0]
        event_details['description'] = 'For more information, please visit: ' + event.h2.a.get('href')
        print(event_details)
    
def get_crazy_horse_urls():
    r = requests.get('http://crazyhorsenc.com/about/live-music/')
    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all(class_="tribe-events-pro-photo__event-title-link")
    urls = []
    
    for url in links:
        urls.append(url.get('href'))

    return urls

def get_crazy_horse_data():
    urls = get_crazy_horse_urls()
    data = []

    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        datetime_str = soup.find(class_='tribe-event-date-start').get_text()
        date = datetime_str.split('/')[0].strip()
        start_time = datetime_str.split('/')[-1].strip()
        end_time = soup.find(class_='tribe-event-time').get_text()
        cost = soup.find(class_='tribe-events-cost').get_text().split('/')[-1].strip()

        event_details = {
            'title': soup.h1.get_text(),
            'location': 'Crazy Horse Saloon & Grill',
            'date': convert_date(date),
            'start_time': convert_time(start_time),
            'end_time': convert_time(end_time),
            'cost': cost
        }

        data.append(event_details)

    return data

def get_all_scraper_events():
    mf_events = get_miners_foundry_data()
    ch_events = get_crazy_horse_data()

    return mf_events + ch_events