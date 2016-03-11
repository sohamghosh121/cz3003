from django.contrib.auth import authenticate, login as dologin

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required

import os
from tabview import TabViews


def healthCheck(request):
    return HttpResponse('It\'s all good!')


@login_required
def render_tab_view(request, tabs, data={}):
    active_tab = tabs.get_active_tab()
    partner = Partner.objects.get(id=1)
    if active_tab:
        return render(request, active_tab.template,
                      {'title': active_tab.title,
                       'data': data,
                       'tabs': tabs.tabs,
                       'partner_name': partner.name})
    else:
        return HttpResponse('ERROR')

def login_view(request):

def my_view(request):
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
def logout_view(request):
  logout(request)
  return redirect('google.com.sg')
  
def submit_event(request):
def map_view(request):
def list_event_view(request)