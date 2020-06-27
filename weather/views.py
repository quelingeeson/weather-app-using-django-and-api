from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d2ed5bee74b4a148b3f48ec48a2ce566'

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()
    data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'name': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],

        }

        data.append(city_weather)

    context = {'city_weather': data, 'form': form}

    return render(request, "weather/weather.html", context)
