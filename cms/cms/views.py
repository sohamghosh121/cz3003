from django.contrib.auth import authenticate, login as dologin

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from models import Operator, Admin

from pullapis.weather import WeatherAPI
from pullapis.dengue import DengueAPI

import os
from tabview import TabViews


def isUserType(user, usercls):
    try:
        u = usercls.objects.get(user_ptr=user.id)
        return True
    except:
        return False


def isOperator(user):
    return isUserType(user, Operator)


def isAdmin(user):
    return isUserType(user, Admin)


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


def registerOperator(request, username, email, password):
    if not isOperator(Operator.objects.all(), username):
        newOperator = Operator.objects.create_user(username, email, password)
        newOperator.save()
        return HttpResponse("Operator created!")
    return HttpResponse("Operator existed!")


def loginView(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            dologin(request, user)
            if isOperator(user):  # login as an operator
                return redirect('/operator/map')
            elif isAdmin(user):  # login as an admin
                return redirect('/admin/map')
        else:
            # Return a 'disabled account' error message
            return HttpResponse("Disabled account")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Invalid login")


def logoutView(request):
    logout(request)
    return redirect('/login')


def submit_event(request):
    return None


def map_view(request):
    return None


def list_event_view(request):
    return None


def getWeatherInfo(request):
    return JsonResponse(WeatherAPI().returnGeoJson(), safe=False)


def getDengueInfo(request):
    return JsonResponse(DengueAPI().returnGeoJson(), safe=False)
