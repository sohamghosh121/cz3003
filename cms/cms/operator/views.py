from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from ..views import renderTabView
from django.contrib.gis.geos import Point
from ..models import TrafficEvent, TerroristEvent, Event, EventTransactionLog, Operator
from tabview import OperatorTabViews


def healthCheck(request):
    return HttpResponse('It\'s all good! Operator UI works :)')


def latLngToPoint(stringobj):
    lat, lng = stringobj.split(',')
    return Point(float(lng), float(lat))

# @login_required


def newEvent(request):
    if request.method == 'GET':
        tabs = OperatorTabViews()
        tabs.set_active_tab('newevent')
        data = {
            'eventtypes': enumerate(['Traffic Event', 'Terrorist Event'])
        }
        return renderTabView(request, tabs, data)
    elif request.method == 'POST':
        eventDetails = {}
        eventtype = request.POST.get('eventtype')
        eventDetails['name'] = request.POST.get('name')
        eventDetails['operator'] = Operator.objects.get(user_ptr_id=1)
        eventDetails['contact_number'] = request.POST.get('contact')
        eventDetails['description'] = request.POST.get('description')
        eventDetails['num_casualties'] = int(request.POST.get('numCasualties'))
        eventDetails['num_injured'] = int(request.POST.get('numInjured'))
        eventDetails['location'] = latLngToPoint(request.POST.get('location'))
        event = Event.objects.create(**eventDetails)
        event.save()
        eventlog = EventTransactionLog.objects.create(
            event=event, transaction_type='CR', operator=Operator.objects.get(user_ptr_id=1))  # add the operator in later
        eventlog.save()
        if eventtype:
            specificEventDetails = {'event': event}
            if eventtype == 'traffic':
                specificEventDetails['num_vehicles'] = int(
                    request.POST.get('numVehicles'))
                newEvent = TrafficEvent.objects.create(**specificEventDetails)
            elif eventtype == 'terrorist':
                specificEventDetails['num_hostiles'] = int(
                    request.POST.get('numHostiles'))
                specificEventDetails[
                    'attack_type'] = request.POST.get('attacktype')
                newEvent = TerroristEvent.objects.create(**specificEventDetails)
            else:
                return HttpResponseBadRequest('nnok')
            newEvent.save()
            return HttpResponse('ok')
        return HttpResponseBadRequest('nok')


def listEvents(request):
    tabs = OperatorTabViews()
    tabs.set_active_tab('list')
    return renderTabView(request, tabs, {
        'trafficevents': TrafficEvent.objects.all(),
        'terroristevents': TerroristEvent.objects.all()
    })


def mapEvents(request):
    tabs = OperatorTabViews()
    tabs.set_active_tab('map')
    return renderTabView(request, tabs, {})


def getEventType(event):
    if isinstance(event, TrafficEvent):
        return 'traffic'
    elif isinstance(event, TerroristEvent):
        return 'terrorist'


def getEvents(request):
    events_list = []
    events_list.extend(TrafficEvent.objects.all())
    events_list.extend(TerroristEvent.objects.all())
    events_list = [{
        'type': getEventType(e),
        'details': e
    }
        for e in sorted(events_list, key=lambda x: x.event.date_recorded, reverse=True)
    ]
    return events_list


def getEventTypeIcon(eventtype):
    if eventtype == 'traffic':
        return '/static/img/caraccident.png'
    elif eventtype == 'terrorist':
        return '/static/img/terrorist.png'


def getEventsGeoJSON(request):
    data = {}
    geojson = {'type': 'FeatureCollection', 'features': []}
    events = getEvents(request)
    geojson['features'] = [{
        'type': 'Feature',
        'geometry': {
                'type': 'Point',
                'coordinates': [event['details'].event.location.x, event['details'].event.location.y]
        },
        'properties': {
            'type': event['type'],
            'icon': getEventTypeIcon(event['type'])
        }
    } for event in events]
    data['geojson'] = geojson
    return JsonResponse(data, safe=False)

def pull_weather(request):
    return JsonResponse(WeatherAPI().returnGeoJson(), safe=False)
