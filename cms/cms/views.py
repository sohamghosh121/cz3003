from django.contrib.auth import authenticate, login as dologin

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point

import os
from tabview import TabViews, OperatorTabViews
from models import TrafficEvent, TerroristEvent, Operator


def healthCheck(request):
    return HttpResponse('It\'s all good!')


def renderTabView(request, tabs, data={}):
    active_tab = tabs.get_active_tab()
    if active_tab:
        return render(request, active_tab.template,
                      {'title': active_tab.title,
                       'data': data,
                       'tabs': tabs.tabs})
    else:
        return HttpResponse('ERROR')


def latLngToPoint(stringobj):
    lat, lng = stringobj.split(',')
    return Point(float(lng), float(lat))


@login_required
def newEvent(request):
    if request.method == 'GET':
        tabs = OperatorTabViews()
        tabs.set_active_tab('newevent')
        data = {
            'eventtypes': enumerate(['Traffic Event', 'Terrorist Event'])
        }
        return renderTabView(request, tabs, data)
    elif request.method == 'POST':
        event = {}
        eventtype = request.POST.get('eventtype')
        event['name'] = request.POST.get('name')
        event['operator'] = Operator.objects.get(id=1)
        event['contact_number'] = request.POST.get('contact')
        event['description'] = request.POST.get('description')
        event['num_casualties'] = int(request.POST.get('numCasualties'))
        event['num_injured'] = int(request.POST.get('numInjured'))
        event['location'] = latLngToPoint(request.POST.get('location'))
        if eventtype:
            if eventtype == 'traffic':
                event['num_vehicles'] = int(request.POST.get('numVehicles'))
                newEvent = TrafficEvent.objects.create(**event)
            elif eventtype == 'terrorist':
                event['num_hostiles'] = int(request.POST.get('numVehicles'))
                event['attack_type'] = request.POST.get('attackType')
                newEvent = TerroristEvent.objects.create(**event)
            else:
                return HttpResponseBadRequest('nnok')
            newEvent.save()
            return HttpResponse('ok')
        return HttpResponseBadRequest('nok')


def loginView(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('google.com.sg')
        else:
            # Return a 'disabled account' error message
            return HttpResponse("Disabled account")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Invalid login")


def logoutView(request):
    logout(request)
    return redirect('google.com.sg')


def submit_event(request):
    return None


def map_view(request):
    return None


def list_event_view(request):
    return None
