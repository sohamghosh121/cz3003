from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from ..views import renderTabView, isOperator, isAdmin
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.contrib.auth.decorators import login_required
from ..models import TrafficEvent, TerroristEvent, Event, EventTransactionLog, Operator, Reporter, Haze
from ..dispatchers.agencydispatcher import AgencyDispatcher
from tabview import OperatorTabViews
from ..pullapis.dengue import DengueAPI
from ..pullapis.weather import WeatherAPI

def healthCheck(request):
    return HttpResponse('It\'s all good! Operator UI works :)')


def latLngToPoint(stringobj):
    lat, lng = stringobj.split(',')
    return Point(float(lng), float(lat))


@login_required
def deactivateEvent(request):
    if not isOperator(request.user):
        return HttpResponseBadRequest()
    eventid = request.GET.get('eventid')
    e = Event.objects.get(id=eventid)
    e.isactive = False
    e.save()
    operator = Operator.objects.get(user_ptr_id=request.user.id)
    eventlog = EventTransactionLog.objects.create(
        event=e,
        transaction_type='ED',
        operator=operator,
        desc='DEACTIVATE event')
    eventlog.save()
    AgencyDispatcher(eventlog).dispatch()
    return redirect('/operator/list')


@login_required
def updateEvent(request):
    if not isOperator(request.user):
        return HttpResponseBadRequest()
    if request.method == 'POST':
        reporter = {}
        eventtype = request.POST.get('eventtype')
        event_id = request.POST.get('eventid')
        reporter['identification'] = request.POST.get('identification')
        try:
            reporter = Reporter.objects.get(
                identification=reporter['identification'])
        except Reporter.DoesNotExist:
            reporter['name'] = request.POST.get('name')
            reporter['contact_number'] = request.POST.get('contact')
            reporter = Reporter.objects.create(
                **reporter)
            reporter.save()
        edit_string = []
        if eventtype == 'traffic':
            event = TrafficEvent.objects.get(id=event_id)
            if event.num_vehicles != int(request.POST.get('numVehicles')):
                event.num_vehicles = int(request.POST.get('numVehicles'))
                edit_string.append('UPDATE num_vehicles')
        elif eventtype == 'terrorist':
            event = TerroristEvent.objects.get(id=event_id)
            if event.num_hostiles != int(request.POST.get('numHostiles')):
                event.num_hostiles = int(request.POST.get('numHostiles'))
                edit_string.append('UPDATE num_hostiles')
        if event.event.num_casualties != int(request.POST.get('numCasualties')):
            event.event.num_casualties = int(request.POST.get('numCasualties'))
            edit_string.append('UPDATE num_casualties')
        if event.event.num_injured != int(request.POST.get('numInjured')):
            event.event.num_injured = int(request.POST.get('numInjured'))
            edit_string.append('UPDATE num_injured')
        if event.event.description != request.POST.get('description'):
            event.event.description = request.POST.get('description')
            edit_string.append('UPDATE description')
        event.event.save()
        event.save()
        operator = Operator.objects.get(user_ptr_id=request.user.id)
        if operator not in event.event.operator.all():
            event.event.operator.add(operator)
        if reporter not in event.event.reporters.all() or reporter != event.event.first_responder:
            event.event.reporters.add(reporter)
        eventlog = EventTransactionLog.objects.create(
            event=event.event,
            transaction_type='ED',
            operator=operator,
            reporter=reporter,
            desc=','.join(edit_string))
        eventlog.save()
        AgencyDispatcher(eventlog).dispatch()  # dispatch to agencies
        return redirect('/operator/list')
    else:
        return HttpResponseBadRequest()


@login_required
def newEvent(request):
    if not isOperator(request.user):
        return HttpResponseBadRequest()
    if request.method == 'GET':
        tabs = OperatorTabViews()
        tabs.set_active_tab('newevent')
        data = {
            'eventtypes': enumerate(['Traffic Event', 'Terrorist Event'])
        }
        return renderTabView(request, tabs, data)
    elif request.method == 'POST':
        eventDetails = {}
        reporter = {}
        eventtype = request.POST.get('eventtype')
        reporter['identification'] = request.POST.get('identification')
        try:
            eventDetails['first_responder'] = Reporter.objects.get(
                identification=reporter['identification'])
        except Reporter.DoesNotExist:
            reporter['name'] = request.POST.get('name')
            reporter['contact_number'] = request.POST.get('contact')
            eventDetails['first_responder'] = Reporter.objects.create(
                **reporter)
            eventDetails['first_responder'] .save()

        operator = Operator.objects.get(user_ptr_id=request.user.id)
        eventDetails['description'] = request.POST.get('description')
        eventDetails['num_casualties'] = int(request.POST.get('numCasualties'))
        eventDetails['num_injured'] = int(request.POST.get('numInjured'))
        eventDetails['location'] = latLngToPoint(request.POST.get('location'))
        event = Event.objects.create(**eventDetails)
        event.save()
        event.operator.add(operator)

        eventlog = EventTransactionLog.objects.create(
            event=event, transaction_type='CR', operator=operator)  # add the operator in later
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
            AgencyDispatcher(eventlog).dispatch()
            return HttpResponse('ok')
        return HttpResponseBadRequest('nok')


@login_required
def listEvents(request):
    if not isOperator(request.user):
        return HttpResponseBadRequest()
    tabs = OperatorTabViews()
    tabs.set_active_tab('list')
    return renderTabView(request, tabs, {
        'trafficevents': TrafficEvent.objects.filter(event__isactive=True),
        'terroristevents': TerroristEvent.objects.filter(event__isactive=True)
    })


# @login_required
def mapEvents(request):
    # if not isOperator(request.user):
    #     return HttpResponseBadRequest()
    tabs = OperatorTabViews()
    tabs.set_active_tab('map')
    return renderTabView(request, tabs, {'haze': Haze.objects.all()})


def getEventType(event):
    if isinstance(event, TrafficEvent):
        return 'traffic'
    elif isinstance(event, TerroristEvent):
        return 'terrorist'


def getEventUpdateForm(request):
    if not isOperator(request.user):
        return HttpResponseBadRequest()
    context = {}
    event_id = request.GET.get('eventid')
    context['eventtype'] = request.GET.get('eventtype')
    if context['eventtype'] == 'traffic':
        context['event'] = TrafficEvent.objects.get(id=event_id)
    elif context['eventtype'] == 'terrorist':
        context['event'] = TerroristEvent.objects.get(id=event_id)
    else:
        return HttpResponseBadRequest()
    return render(request, 'operator/updateEventForm.html', context)


def getEvents(request):
    if not isOperator(request.user):
        return HttpResponseBadRequest()
    events_list = []
    events_list.extend(TrafficEvent.objects.filter(event__isactive=True))
    events_list.extend(TerroristEvent.objects.filter(event__isactive=True))
    events_list = [{
        'type': getEventType(e),
        'details': e
    }
        for e in sorted(events_list, key=lambda x: x.event.date_recorded, reverse=True)
    ]
    return events_list


def getEventTypeIcon(eventtype):
    if eventtype == 'traffic':
        return 'caraccident.png'
    elif eventtype == 'terrorist':
        return 'terrorist.png'


def getEventsGeoJSON(request):
    if not isOperator(request.user):
        return HttpResponseBadRequest()
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
            'icon': getEventTypeIcon(event['type']),
            'event': {
                'name': event['details'].event.first_responder.name,
                'description': event['details'].event.description,
                'operator': event['details'].event.operator.all()[0].name
            }
        }
    } for event in events]
    data['geojson'] = geojson
    return JsonResponse(data, safe=False)


def pull_weather(request):
    return JsonResponse(WeatherAPI().returnGeoJson(), safe=False)

def refreshAPI(request):
    WeatherAPI().pullWeatherUpdate()
    DengueAPI().pullUpdate()
    WeatherAPI().pullPSIUpdate()
    return HttpResponse('ok')
