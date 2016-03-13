from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from cms.models import TrafficEvent, TerroristEvent, Districts
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import time
import requests


def getTrafficInfo(request):
    trafficEvents = TrafficEvent.objects.all()
    response = {}
    numVehicles = 0
    numCasualties = 0
    numInjuries = 0
    for trafficEvent in trafficEvents:
        event = trafficEvent.event
        numVehicles += trafficEvent.num_vehicles
        numCasualties += event.num_casualties
        numInjuries += event.num_injured
    response['numTraffics'] = len(trafficEvents)
    response['numVehicles'] = numVehicles
    response['numCasualties'] = numCasualties
    response['numInjuries'] = numInjuries

    return JsonResponse(response, safe=False)


def getTerroristInfo(request):
    terroristEvents = TerroristEvent.objects.all()
    response = {}
    numHostiles = 0
    numCasualties = 0
    numInjuries = 0
    attackTypes = ""
    for terroristEvent in terroristEvents:
        event = terroristEvent.event
        numHostiles += terroristEvent.num_hostiles
        numCasualties += event.num_casualties
        numInjuries += event.num_injured
        attackTypes += terroristEvent.attack_type +','

    response['numAttacks'] = len(terroristEvents)
    response['numHostiles'] = numHostiles
    response['numCasualties'] = numCasualties
    response['numInjuries'] = numInjuries
    response['attackTypes'] = attackTypes

    return JsonResponse(response, safe=False)

def getCrisisInfo(request):
    districts = Districts.objects.all()
    response = {}
    for d in districts:
        response[d.district] = d.crisis
    return JsonResponse(response, safe=False)


def getMapImage(request):
    try:
        print 'capturing screenshots'
        # browser = webdriver.Firefox()
        # browser.get('http://localhost:8000/maps/crisis')
        # element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        # browser.save_screenshot('cms/static/img/crisis_screenshot.png')
        # browser.get('http://localhost:8000/maps/traffic')
        # element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        # browser.save_screenshot('cms/static/img/traffic_screenshot.png')
        # browser.get('http://localhost:8000/maps/terrorist')
        # element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        # browser.save_screenshot('cms/static/img/terrorist_screenshot.png')
        # browser.get('http://localhost:8000/maps/weather')
        # element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        # browser.save_screenshot('cms/static/img/weather_screenshot.png')
        # browser.get('http://localhost:8000/maps/dengue')
        # element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        # browser.save_screenshot('cms/static/img/dengue_screenshot.png')
        # browser.quit()
    finally:
        return HttpResponse('done')
