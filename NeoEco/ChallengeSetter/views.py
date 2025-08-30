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

import requests
import json
import re

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

