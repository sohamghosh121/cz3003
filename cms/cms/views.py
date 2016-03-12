from django.contrib.auth import authenticate, login as dologin

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point

import os
from tabview import TabViews
# from models import TrafficEvent, TerroristEvent, Operator


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
