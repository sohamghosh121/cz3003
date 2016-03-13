from django.contrib.auth import authenticate, login as dologin, logout

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
        if isOperator(request.user):
            return 'Operator'
        elif isAdmin(request.user):
            return 'Admin'

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
