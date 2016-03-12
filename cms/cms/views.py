from django.contrib.auth import authenticate, login as dologin

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from models import Operator, Admin

from pullapis.weather import WeatherAPI

import os
from tabview import TabViews

operatorList = Operator.objects.all()
adminList = Admin.objects.all()

def isOperator(operatorList, username):
    for operator in operatorList:
        if operator.username == username:
            return True
    return False

def isAdmin(adminList, username):
    for admin in adminList:
        if admin.username == username:
            return True
    return False

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

def registerOperator(request,username,email,password):
    if not isOperator(operatorList,username):
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
            if isOperator(operatorList, username): #login as an operator
                return redirect('https://www.google.com.sg/')
            elif isAdmin(adminList, username): #login as an admin
                return redirect('https://www.facebook.com/')
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

def pullWeatherInfo(request):
    return JsonResponse(WeatherAPI().returnGeoJson(), safe=False)
