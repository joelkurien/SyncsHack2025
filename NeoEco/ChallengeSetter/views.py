import random
import time
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import requests
import pandas as pd
import math
import asyncio, httpx
import os
from dotenv import load_dotenv
import json
from .models import User

load_dotenv("./content.env")

GROQ_API = os.getenv("GROQ_API")
WEATHER_API = os.getenv("WEATHER_KEY")
TRAFFIC_API = os.getenv("TRAFFIC_KEY")

currentUser = None

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

@api_view(['POST'])
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    address = request.data.get("address1")
    work_address = request.data.get("address2")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=username,
        email=email,
        password=password,  # important: never store raw passwords
        address = address,
        work_address = address
    )

    return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "Wrong Username"}, status=status.HTTP_401_UNAUTHORIZED)

    if user.check_password(password):
        return Response({"error": "Wrong Password"}, status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)

    currentUser = user
    return Response({
        "message": "Login successful",
        "token": token.key,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "eco_rank": user.eco_rank,
            "xp": user.xp,
            "level": user.level,
            "avatar_choice": user.avatar_choice,
        }
    }, status=status.HTTP_200_OK)

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
    
@api_view(['GET'])
def search_opportunities(location=None):
    
    API_ENDPOINT = 'https://www.volunteerconnector.org/api/search/'
    final_query = 'environment'
    if location:
        final_query += f' {location}'

    params = {'q': final_query}
    try:
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()  

        data = response.json()

        volunteerTasks = []
        if data.get('results'):
            for opportunity in data['results']:
                description = opportunity.get('description', 'No description available.')
                url = opportunity.get('url', 'No URL available')
                volunteer = {
                    "title": opportunity.get('title', 'No Title Provided'),
                    "orgName": opportunity.get('organization', {}).get('name', 'Unknown Organization'),
                    "url": url,
                    "description": f"{description[:50]}... More Info at {url}"
                }
                volunteerTasks.append(volunteer)
        else:
            raise ValueError("No volunteer opportunities found with that search criteria.")
        return Response({
            "type":"volunteer_quests",
            "results": volunteerTasks
        })

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return Response({
            "type":"volunteer_quests",
            "results": []
        })
    except json.JSONDecodeError:
        print("Failed to decode JSON response from the API.")
        return Response({
            "type":"volunteer_quests",
            "results": []
        })
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return Response({
            "type":"volunteer_quests",
            "results": []
        })


SKILL_TREE = [
    {"name": "Daily Challenge Streak Bonus", "unlock_level": 5},
    {"name": "Double Points Weekend", "unlock_level": 10},
    
]

def grant_daily_streak_bonus(user):
    """
    Grant XP bonus for daily challenge streaks if the user has unlocked the skill.
    
    Args:
        user: User instance to grant bonus to
    """
    if user.level >= 5:  # Check if user has reached level 5 to unlock the skill
        user.xp += 20
        user.save()
        return True
    return False

@api_view(['POST'])
def complete_quest(request):
    fileUpload = request.FILES.get('file')
    if not fileUpload:
        return Response({"error": "No file or invalid file"}, status=400)

    currentUser.quest_file_name = fileUpload.name
    xpGain = random.randint(10,50)
    
    currentUser.xp += xpGain
    last_quest_id = User.objects.order_by('-quest_id').first()
    currentUser.quest_id = request.data.get('quest_id') if request.data.get('quest_id') else f"quest_{random.randint(1000, 9999)}"

    time.sleep(5)
    currentUser.quest_completed = True

    # Continuous level system
    currentUser.level = currentUser.xp // 50   # 1 level every 50 XP
    if currentUser.level == 0:
        currentUser.level = 1  # Ensure minimum level is 1

    # Rank system (based on XP milestones)
    if currentUser.xp < 250:
        currentUser.rank = "Bronze"

    elif currentUser.xp < 500:
        currentUser.rank = "Silver"

    elif currentUser.xp < 1000:
        currentUser.rank = "Gold"

    else:
        currentUser.rank = "Amethyst"


    currentUser.save()


    
    return Response({
        "message": "File uploaded successfully",
        "xp_gain": xpGain,
        "new_xp": currentUser.xp,
        "quest_id": currentUser.quest_id,
        "new_rank": currentUser.rank,
        "new_level": currentUser.level
    })
    
def check_skill_unlocks(user):
    """
    Check and unlock new skills based on user level.
    
    Args:
        user: User instance to check skills for
        
    Returns:
        list: Newly unlocked skills
    """
    newly_unlocked = []
    
    for skill in SKILL_TREE:
        if user.level >= skill["unlock_level"]:
            # You can add logic here to actually unlock skills
            # For now, we'll just return the skill names
            newly_unlocked.append(skill["name"])
    
    return newly_unlocked

def get_user_stats(user):
    """
    Get comprehensive user statistics.
    
    Args:
        user: User instance to get stats for
        
    Returns:
        dict: User statistics
    """
    return {
        "username": user.username,
        "level": user.level,
        "xp": user.xp,
        "eco_rank": user.eco_rank,
        "progress_to_next_level": xp_progress(user),
        "unlocked_skills": check_skill_unlocks(user),
        "date_joined": user.date_joined,
        "last_login": user.last_login
    }

