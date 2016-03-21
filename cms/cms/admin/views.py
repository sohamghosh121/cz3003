from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from ..models import TrafficEvent, TerroristEvent, Event, EventTransactionLog, Operator, Singapore, CrisisTransactionLog, Haze
from tabview import AdminTabViews
from ..views import render_tab_view, is_operator, is_admin
from ..districts.districts import DistrictManager, CrisisManager
from django.template.defaulttags import register
import json, requests
from django.contrib.auth.decorators import login_required

# def healthCheck(request):
#     return HttpResponse('It\'s all good! Admin UI works :)')

def get_transaction_log(request):
    tabs = AdminTabViews()
    tabs.set_active_tab('log')
    event_type_dict = {}
    return render_tab_view(request, tabs, {
        'event_transaction_log': EventTransactionLog.objects.all(),
        'crisis_log_database': CrisisTransactionLog.objects.all(),
    })

def get_crisis_view(request):
    """
        Set crisis manager as active tab
    """
    tabs = AdminTabViews()
    tabs.set_active_tab('crisis')
    return render_tab_view(request, tabs, {
    })

@register.filter(name = 'type')
def get_event_type(log):
    if (TrafficEvent.objects.filter(event=log.event).exists() == True):
        return 'Traffic'
    if (TerroristEvent.objects.filter(event=log.event).exists() == True):
        return 'Terrorist'
    return None

@register.filter (name = 'address')
def get_address_from_lat_long(latlong):
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false" % (latlong.y,latlong.x)
    r = requests.get(url)
    result = r.json()
    address = ""
    for x in result.get('results')[0].get('address_components'):
        address += x.get('long_name') +', '
    return address [:-2]

@register.filter (name = 'tran')
def get_long_transaction_type(log):
    return log.get_transaction_type_display()

@register.filter (name = 'adminop')
def get_admin_or_operator(log):
    if log.operator is not None:
        return log.operator
    if log.admin is not None:
        return log.admin
    return '-'

def get_districts(request):
    return JsonResponse(DistrictManager().return_geo_json(), safe=False)

@login_required
def set_crisis(request):
    if not is_admin(request.user):
        return HttpResponseBadRequest()
    CrisisManager().set_crisis_level(request.GET.get('district'), request.GET.get('newcrisis'), None)
    return HttpResponse("Success", content_type="text/plain")

def map_events(request):
    # if not isOperator(request.user):
    #     return HttpResponseBadRequest()
    tabs = AdminTabViews()
    tabs.set_active_tab('map')
    return render_tab_view(request, tabs, {'haze': Haze.objects.all()})

@login_required
def list_events(request):
    if not is_admin(request.user):
        return HttpResponseBadRequest()
    tabs = AdminTabViews()
    tabs.set_active_tab('list')
    return render_tab_view(request, tabs, {
        'trafficevents': TrafficEvent.objects.filter(event__isactive=True),
        'terroristevents': TerroristEvent.objects.filter(event__isactive=True)
    })

@login_required
def delete_event(request):
    if not is_admin(request.user):
        return HttpResponseBadRequest()
    if request.method == 'GET':
        event_id = request.GET.get('eventid')
        event_type = request.GET.get('eventtype')
        if (event_type == 'traffic'):
            t = TrafficEvent.objects.get(id = event_id)
            e = Event.objects.get(id = t.event.id)
            e.delete()
        elif (event_type == 'terrorist'):
            t = TerroristEvent.objects.get(id = event_id)
            print t.event.id
            e =Event.objects.get(id = t.event.id)
            e.delete()
        return HttpResponse("Success", content_type="text/plain")