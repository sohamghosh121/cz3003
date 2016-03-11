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
