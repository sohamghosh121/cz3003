from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from ..models import TrafficEvent, TerroristEvent, Event, EventTransactionLog, Operator, Singapore, CrisisTransactionLog
from tabview import AdminTabViews
from ..views import renderTabView
from ..districts.districts import DistrictManager, CrisisManager
from django.template.defaulttags import register
import json, requests

def healthCheck(request):
    return HttpResponse('It\'s all good! Admin UI works :)')

def getTransactionLog(request):
	tabs = AdminTabViews()
	tabs.set_active_tab('log')
	eventTypeDict = {}
	return renderTabView(request, tabs, {
        'eventTransactionLog': EventTransactionLog.objects.all(),
        'crisisLogDatabase': CrisisTransactionLog.objects.all(),
    })

def getCrisisView(request):
	"""
		Set crisis manager as active tab
	"""
	tabs = AdminTabViews()
	tabs.set_active_tab('crisis')
	return renderTabView(request, tabs, {
    })

@register.filter(name = 'type')
def getEventType(log):
	if (TrafficEvent.objects.filter(event=log.event).exists() == True):
		return 'Traffic'
	if (TerroristEvent.objects.filter(event=log.event).exists() == True):
		return 'Terrorist'
	return None

@register.filter (name = 'address')
def getAddressFromLatLong(latlong):
	url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false" % (latlong.y,latlong.x)
	r = requests.get(url)
	result = r.json()
	address = ""
	for x in result.get('results')[0].get('address_components'):
		address += x.get('long_name') +', '
	return address [:-2]

@register.filter (name = 'tran')
def getLongTransactionType(log):
	return log.get_transaction_type_display()

@register.filter (name = 'adminop')
def getAdminOrOperator(log):
	if log.operator is not None:
		return log.operator
	if log.admin is not None:
		return log.admin
	return '-'

def getDistricts(request):
	return JsonResponse(DistrictManager().returnGeoJson(), safe=False)

def setCrisis(request):
	CrisisManager().setCrisisLevel(request.GET.get('district'), request.GET.get('newcrisis'), None)
	return HttpResponse("Success", content_type="text/plain")
	