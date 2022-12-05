from django.shortcuts import render, redirect
import requests
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from django.contrib import messages

from .forms import IndexForm

def index(request):
    form = IndexForm()
    context = {
        'form': form,
    }
    return render(request, 'index.html', context)


def forecast(request):

   if str(request.method) == 'POST':
        form = IndexForm(request.POST)

        if form.is_valid():

            #locator = Nominatim(user_agent='myGeocoder')
            #location = locator.geocode('aracaju')

            lat = form.cleaned_data.get('lat')
            lon = form.cleaned_data.get('lon')

            api_key = '###########################'
            units = 'metric'
            lang = 'pt_br'

            results = requests.get(url=f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units={units}&lang={lang}').json()


            # Corrigindo o fuso horário e o formato da data
            for date_time in results['list']:
                date_time_dt = datetime.strptime(date_time['dt_txt'], '%Y-%m-%d %H:%M:%S')
                date_time_local = date_time_dt + timedelta(hours=int(results['city']['timezone'])/3600)
                date_time['dt_txt'] = str(date_time_local.strftime('%d/%m/%Y - %H:%M:%S'))
         
            context = {
                'results': results,
            }

            return render(request, 'forecast.html', context)

        else:
            messages.error(request, 'A Latitude de estar entre -90 e 90, e a Longitude entre -180 e 180!')
            return redirect('index')