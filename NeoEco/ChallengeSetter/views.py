from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def decideTransportOperation(request):
    pass

def getLatLong(location):
    try:
        url = "https://photon.komoot.io/api/"
        params={"q": location, "limit": 1}
        latlongResp = requests.get(url, params=params)
        data = latlongResp.json()
        
        if data and data['features']:
            points = data['features'][0]['geometry'].get("coordinates")
            long, lat = points[0], points[1]
            return [long, lat]
        else:
            raise ValueError("Location is inValid")
    except Exception as e:
        return None

