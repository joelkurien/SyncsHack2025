from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json

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



def search_opportunities(location=None):
    """
    Searches the VolunteerConnector API for volunteer opportunities related to "environment"
    and a specific location, and then prints the details of the jobs found.

    Args:
        location (str, optional): A city or postal code to filter by location.
    """
    
    API_ENDPOINT = 'https://www.volunteerconnector.org/api/search/'
    
    # We will search broadly for "environment" and combine it with the location
    final_query = 'environment'
    if location:
        final_query += f' {location}'

    params = {'q': final_query}

    print(f"Searching for all '{final_query}' opportunities...")
    print("-" * 60)

    try:
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4xx or 5xx

        data = response.json()

        if data.get('results'):
            print("Volunteer opportunities found:")
            print("-" * 60)
            for opportunity in data['results']:
                title = opportunity.get('title', 'No Title Provided')
                organization_name = opportunity.get('organization', {}).get('name', 'Unknown Organization')
                url = opportunity.get('url', 'No URL available')
                description = opportunity.get('description', 'No description available.')
                
                print(f"Title: {title}")
                print(f"Organization: {organization_name}")
                print(f"URL: {url}")
                print(f"Description: {description[:150]}...")  # Truncate description for readability
                print("-" * 60)
        else:
            print("No volunteer opportunities found with that search criteria.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON response from the API.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


SKILL_TREE = [
    {"name": "Daily Challenge Streak Bonus", "unlock_level": 5},
    {"name": "Double Points Weekend", "unlock_level": 10},
    # Add more skills as needed
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

def xp_progress(user):
    """
    Calculate progress percentage to next level.
    
    Args:
        user: User instance to calculate progress for
        
    Returns:
        float: Progress percentage (0.0 to 1.0)
    """
    try:
        # Define XP thresholds for levels (you can adjust these values)
        level_thresholds = [0, 100, 250, 500, 1000, 2000, 4000, 8000, 16000, 32000]
        
        current_level = user.level
        if current_level >= len(level_thresholds):
            return 1.0  # Max level reached
            
        current_level_xp = level_thresholds[current_level - 1]
        next_level_xp = level_thresholds[current_level]
        
        progress = (user.xp - current_level_xp) / (next_level_xp - current_level_xp)
        return max(0.0, min(1.0, progress))
        
    except Exception as e:
        print(f"Error calculating XP progress: {e}")
        return 0.0

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

