# frontend/views.py
from django.http import HttpResponseServerError
from django.shortcuts import render
import requests

def home(request):
    api_url = 'http://127.0.0.1:8000/api/profiles/'
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        profiles = response.json()
        return render(request, 'home.html', {'profiles': profiles})
    except requests.exceptions.RequestException as e:
        return HttpResponseServerError(f'Error fetching data from API: {e}')
    except ValueError as e:
        return HttpResponseServerError(f'Error decoding JSON: {e}')

def user_detail(request, username):
    api_url = f'http://127.0.0.1:8000/api/profiles/?username={username}'  # URL to fetch details of a specific user
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        profiles = response.json()
        if profiles:
            for profile in profiles:
                if profile['username'] == username:
                    return render(request, 'user_detail.html', {'profile': profile})
            return HttpResponseServerError(f'No profile found for username: {username}')
        else:
            return HttpResponseServerError(f'No profiles found')
    except requests.exceptions.RequestException as e:
        return HttpResponseServerError(f'Error fetching data from API: {e}')
    except ValueError as e:
        return HttpResponseServerError(f'Error decoding JSON: {e}')
