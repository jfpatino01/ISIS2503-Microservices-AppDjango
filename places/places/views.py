from .models import Places
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
import requests
import json

def check_variable(data):
    r = requests.get(settings.PATH_VAR, headers={"Accept":"application/json"})
    variables = r.json()
    for variable in variables:
        if data["variable"] == variable["id"]:
            return True
    return False

def PlacesList(request):
    queryset = Places.objects.all()
    context = list(queryset.values('id', 'variable', 'value', 'unit', 'place', 'dateTime'))
    return JsonResponse(context, safe=False)

def PlaceCreate(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        if check_variable(data_json) == True:
            place = Places()
            place.variable = data_json['variable']
            place.value = data_json['value']
            place.unit = data_json['unit']
            place.place = data_json['place']
            place.save()
            return HttpResponse("successfully created place")
        else:
            return HttpResponse("unsuccessfully created place. Variable does not exist")

def PlacesCreate(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        places_list = []
        for place in data_json:
                    if check_variable(place) == True:
                        db_place = Places()
                        db_place.variable = place['variable']
                        db_place.value = place['value']
                        db_place.unit = place['unit']
                        db_place.place = place['place']
                        places_list.append(db_place)
                    else:
                        return HttpResponse("unsuccessfully created place. Variable does not exist")
        
        Places.objects.bulk_create(places_list)
        return HttpResponse("successfully created places")