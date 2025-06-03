import requests
from django.shortcuts import render
from django.conf import settings

def get_weather_data(city):
    api_key = settings.OPENWEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    return response.json()

def recommend_outfit(temp):
    if temp < 10:
        return "Wear a heavy jacket, scarf, and gloves."
    elif 10 <= temp < 20:
        return "A light jacket and sweater should suffice."
    elif 20 <= temp < 30:
        return "Casual wear like t-shirts and jeans are perfect."
    else:
        return "Stay cool with shorts and a tank top."

def home(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        weather_data = get_weather_data(city)
        if weather_data.get('main'):
            temp = weather_data['main']['temp']
            outfit = recommend_outfit(temp)
            context = {
                'city': city,
                'temp': temp,
                'outfit': outfit,
                'weather': weather_data['weather'][0]['description'],
            }
        else:
            context = {'error': "City not found. Please try again."}
    else:
        context = {}
    return render(request, 'home.html', context)
