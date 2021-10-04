from django import forms
from django.shortcuts import render
import requests

from WeatherApp.forms import CityForm
from .models import City
# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=87004238f4089863cebf1f8c9c22e2bb'
    error = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            exist_city = City.objects.filter(name=new_city).count()
            if exist_city == 0:
                op = requests.get(url.format(new_city)).json()
                print(op)
                if op['cod'] == 200:
                    form.save()
                else:
                    error = "City Does not Exist"
            else:
                error = "City Already Exists in Database"

        if error:
            message = error
            message_class = 'alert-danger'
        else:
            message = "City Added Successfully"
            message_class = 'alert-success'

    form = CityForm()
    city_list = []
    cities = City.objects.all()

    for city in cities:
        op = requests.get(url.format(city)).json()
        
        mycity = {
            'city' : city.name,
            'temp' : op['main']['temp'],
            'desc' : op['weather'][0]['description'],
            'icon' : op['weather'][0]['icon'],
        }

        city_list.append(mycity)
    
    context = {
        'city_list' : city_list,
        'form' : form,
        'message': message,
        'message_class': message_class
        }
    return render(request, 'WeatherApp/home.html', context)