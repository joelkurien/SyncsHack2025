from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import pandas as pd
import math
import asyncio, httpx
import os
from dotenv import load_dotenv

load_dotenv("./content.env")

GROQ_API = os.getenv("GROQ_API")
WEATHER_API = os.getenv("WEATHER_KEY")
TRAFFIC_API = os.getenv("TRAFFIC_KEY")

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

@api_view(['POST'])
def decideTransportOperation(request):
    home = request.data.get("homeAddress")
    target = request.data.get("targetAddress")
    result = asyncio.run(decideTransportOperationAsync(home, target))
    if result:
        return Response({"decision": result})
    else:
        return Response({"decision": "take a car"})

async def decideTransportOperationAsync(home, target):
    async with httpx.AsyncClient(timeout=8) as client:
        startLocation = await getLatLong(client, home)
        targetLocation = await getLatLong(client, target)
        if not startLocation or not targetLocation:
            return None
        distBtPts = distanceBetweenLocations(startLocation, targetLocation)
        
        try:
            trafficCon = getTrafficCondition(client, startLocation, targetLocation)
            weatherCon = weatherCondition(client, targetLocation[0], targetLocation[1])
            traffic, weather = await asyncio.gather(trafficCon, weatherCon)
            
            if not traffic or not weather:
                raise ValueError("No valid Parameters")
            
            decisionParameters = {
                "Average Current Speed": traffic[0],
                "Average Free Flow Speed": traffic[1],
                "Temperature": weather[0],
                "Humidity": weather[1],
                "Description": weather[2], 
                "Wind Speed": weather[3],
                "Distance Between 2 Points": f"{distBtPts} km"
            }
            
            prompt = f'''Decide if the user has to walk, take a bicycle, take a bus, 
                        take a train based on the data provided: {decisionParameters} - give the answer in one word'''
            
            groqPayload ={
                "model": os.getenv("GROQ_MODEL"),
                "messages": [
                    {
                        "role": "user",
                        "content": (prompt)
                    }
                ]
            }
            
            groqUrl = "https://api.groq.com/openai/v1/chat/completions"
            groqHeaders = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API}",
            }

            groqResp = requests.post(groqUrl, headers=groqHeaders, json=groqPayload, timeout=60)
            groqResp.raise_for_status()
            data = groqResp.json()

            # Print the model's reply (one word as requested)
            content = data["choices"][0]["message"]["content"]
            responseJson = {
                "responseTo": "type_of_transport",
                "action": content
            }
            return responseJson

        except Exception as e:
            print("error")
            return None
        

async def getLatLong(client, location):
    try:
        url = "https://photon.komoot.io/api/"
        params={"q": location, "limit": 1}
        latlongResp = await client.get(url, params=params)
        data = latlongResp.json()
        
        if data and data['features']:
            points = data['features'][0]['geometry'].get("coordinates")
            long, lat = points[0], points[1]
            return [lat, long]
        else:
            raise ValueError("Location is inValid")
    except Exception as e:
        return None

def distanceBetweenLocations(startLocation, endLocation):
    startLon = math.radians(startLocation[1])
    endLon = math.radians(endLocation[1])
    startLat = math.radians(startLocation[0])
    endLat = math.radians(endLocation[0])
    lonDiff = endLon - startLon 
    latDiff = endLat - startLat
    val = math.sin(latDiff / 2)**2 + math.cos(startLat) * math.cos(endLat) * math.sin(lonDiff / 2)**2

    c = 2 * math.asin(math.sqrt(val)) 
    r = 6371
    return (c * r)

async def getTrafficCondition(client, startLocation, endLocation):
    try:
        routingUrl = f"https://api.tomtom.com/routing/1/calculateRoute/{startLocation[0]},{startLocation[1]}:{endLocation[0]},{endLocation[1]}/json"
        params = {"traffic": 'true', "key": TRAFFIC_API}
        
        routeResp = await client.get(routingUrl, params=params)
        data = routeResp.json()
        
        if "routes" not in data or len(data['routes']) == 0:
            raise ValueError("No route present")
        
        route = data['routes'][0]
        points = None
        for leg in route.get("legs", []):
            for point in leg.get("points", []):
                points = (point['latitude'], point['longitude'])
        
        if not points:
            raise ValueError("Location is not valid")
        
        flowSegUrl =f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={points[0]},{points[1]}&key={TRAFFIC_API}"
        flowSegResp = await client.get(flowSegUrl)
        data = flowSegResp.json()
        
        flowData = []
        if "flowSegmentData" in data:
            flow = data["flowSegmentData"]
            flowData.append({
                "current_speed": flow.get("currentSpeed", None),
                "free_flow_speed": flow.get("freeFlowSpeed", None)
            })

        if not flowData:
            raise ValueError("There is no flow traffic data available")
        
        flowDf = pd.DataFrame(flowData)

        avgCurrentSpeed = flowDf["current_speed"].mean()
        avgFreeFlowSpeed = flowDf["free_flow_speed"].mean()

        return [avgCurrentSpeed, avgFreeFlowSpeed]
    except Exception as e:
        print("Traffic Break")
        return None
    
async def weatherCondition(client, lat, long):
    try:
        weatherUrl = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={long}&key={WEATHER_API}"
        response = await client.get(weatherUrl)
        data = response.json()

        if "data" in data:
            weather = data["data"][0]
            temperature = weather["temp"]          
            description = weather["weather"]["description"]
            wind_speed = weather["wind_spd"]       
            humidity = weather["rh"]              
            
            return [f"{temperature}%C", f"{humidity}%", description, f"{wind_speed} m/s"]
        raise ValueError("Weather data is not Found")       
        
    except Exception as e:
        print("Weather Break")
        return None
