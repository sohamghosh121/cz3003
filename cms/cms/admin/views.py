from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from ..models import TrafficEvent, TerroristEvent, Event, EventTransactionLog, Operator, Singapore, CrisisTransactionLog
from tabview import AdminTabViews
from ..views import renderTabView
from ..districts.districts import DistrictManager


def healthCheck(request):
    return HttpResponse('It\'s all good! Admin UI works :)')

def getTransactionLog(request):
	tabs = AdminTabViews()
	tabs.set_active_tab('log')
	return renderTabView(request, tabs, {
        'transactionLog': EventTransactionLog.objects.all()
    })

def getCrisisView(request):
	"""
		Set crisis manager as active tab
	"""
	tabs = AdminTabViews()
	tabs.set_active_tab('crisis')
	return renderTabView(request, tabs, {
        'crisisLogDatabase': CrisisTransactionLog
    })

def getDistricts(request):
	return JsonResponse(DistrictManager().returnGeoJson(), safe=False)

# def setCrisis(request):