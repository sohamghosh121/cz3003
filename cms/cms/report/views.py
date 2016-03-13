from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from cms.models import TrafficEvent, TerroristEvent
from selenium import webdriver
import time
import requests


def getTrafficInfo(request):
    trafficEvents = TrafficEvent.objects.all()
    response = {}
    numVehicles = 0
    numCasualties = 0
    numInjuries = 0
    locations = []
    for trafficEvent in trafficEvents:
        event = trafficEvent.event
        numVehicles += trafficEvent.num_vehicles
        numCasualties += event.num_casualties
        numInjuries += event.num_injured
        locations.append(event.location)
    response['numTraffics'] = len(trafficEvents)
    response['numVehicles'] = numVehicles
    response['numCasualties'] = numCasualties
    response['numInjuries'] = numInjuries
    response['locations'] = list(set(locations))

    response['numTraffics'] = 5
    response['numVehicles'] = 15
    response['numCasualties'] = 10
    response['numInjuries'] = 10
    response['locations'] = ['Jurong', 'Orchard']
    return JsonResponse(response, safe=False)


def getTerroristInfo(request):
    terroristEvents = TerroristEvent.objects.all()
    response = {}
    numHostiles = 0
    numCasualties = 0
    numInjuries = 0
    locations = []
    attackTypes = []
    for terroristEvent in terroristEvents:
        event = terroristEvent.event
        numHostiles += event.num_hostiles
        numCasualties += event.num_casualties
        numInjuries += event.num_injured
        locations.append(event.location)
        attackTypes.append(event.attack_type)

    response['numAttacks'] = len(terroristEvents)
    response['numHostiles'] = numHostiles
    response['numCasualties'] = numCasualties
    response['numInjuries'] = numInjuries
    response['locations'] = list(set(locations))
    response['attackTypes'] = list(set(attackTypes))

    response['numAttacks'] = 2
    response['numHostiles'] = 5
    response['numCasualties'] = 10
    response['numInjuries'] = 20
    response['locations'] = ['Orchard', 'Jurong']
    response['attackTypes'] = ['Bomb', 'Biochemical']
    return JsonResponse(response, safe=False)


def getMapImage(request):
    nothing = {}
    browser = webdriver.Firefox()
    browser.get('http://localhost:8000/operator/map')
    time.sleep(2)
    browser.save_screenshot('cms/static/img/map_screenshot.png')
    browser.quit()
    return JsonResponse(nothing, safe=False)
