from django.contrib.auth import authenticate, login as dologin, logout

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from models import Operator, Admin
from models import TrafficEvent, TerroristEvent, Event, EventTransactionLog, Operator, Reporter, Haze
from pullapis.weather import WeatherAPI
from pullapis.dengue import DengueAPI

import os
from tabview import TabViews


def isUserType(user, usercls):
    """
        Check if user is of usercls type
    """
    try:
        u = usercls.objects.get(user_ptr=user.id)
        return True
    except:
        return False


def isOperator(user):
    """
        Check if user is operator
    """
    return isUserType(user, Operator)


def isAdmin(user):
    """
        Check if user is admin
    """
    return isUserType(user, Admin)


def healthCheck(request):
    return HttpResponse('It\'s all good!')


def getUserType(request):
    """
        Get user type if authenticated. If not, user is public.
    """
    if request.user.is_authenticated():
        if isAdmin(request.user):
            return 'Admin'
        elif isOperator(request.user):
            return 'Operator'
    else:
        return 'Public'


def renderTabView(request, tabs, data={}):
    """
        Wrapper method for rendering tab view
    """
    active_tab = tabs.get_active_tab()
    if active_tab:
        return render(request, active_tab.template,
                      {'title': active_tab.title,
                       'data': data,
                       'usertype': getUserType(request),
                       'tabs': tabs.tabs})
    else:
        return HttpResponse('ERROR')


def registerOperator(request, username, email, password):
    """
        Method to create Operator
    """
    if not isOperator(Operator.objects.all(), username):
        newOperator = Operator.objects.create_user(username, email, password)
        newOperator.save()
        return HttpResponse("Operator created!")
    return HttpResponse("Operator existed!")


def loginView(request):
    """
        View function to process login
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            dologin(request, user)
            if isOperator(user):  # login as an operator
                return redirect('/operator/map')
            elif isAdmin(user):  # login as an admin
                return redirect('/admin/map')
            return HttpResponse('ok')
        else:
            # Return a 'disabled account' error message
            return HttpResponse("Disabled account")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Invalid login")


def logoutView(request):
    """
        Process log out action and redirect to login page
    """
    logout(request)
    return redirect('/login')


def getWeatherInfo(request):
    """
        Method to make API call to get GeoJSON Weather data for Google Map. Includes
            - Weather
            - Haze info
    """
    return JsonResponse(WeatherAPI().returnGeoJson(), safe=False)


def getDengueInfo(request):
    """
        Method to make API call to get GeoJSON Dengue data. Includes
            - Dengue hotzones
    """
    return JsonResponse(DengueAPI().returnGeoJson(), safe=False)


def refreshAPI(request):
    WeatherAPI().pullWeatherUpdate()
    DengueAPI().pullUpdate()
    WeatherAPI().pullPSIUpdate()
    return HttpResponse('ok')


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


def getEventType(event):
    if isinstance(event, TrafficEvent):
        return 'traffic'
    elif isinstance(event, TerroristEvent):
        return 'terrorist'
