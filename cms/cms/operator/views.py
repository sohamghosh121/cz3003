from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from ..views import renderTabView
from tabview import OperatorTabViews


def healthCheck(request):
    return HttpResponse('It\'s all good! Operator UI works :)')


def latLngToPoint(stringobj):
    lat, lng = stringobj.split(',')
    return Point(float(lng), float(lat))

# @login_required


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


def listEvents(request):
    tabs = OperatorTabViews()
    tabs.set_active_tab('list')
    return renderTabView(request, tabs, {})


def mapEvents(request):
    tabs = OperatorTabViews()
    tabs.set_active_tab('map')
    return renderTabView(request, tabs, {})
