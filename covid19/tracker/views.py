from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

from .models import *

import requests
import json
import ssl
import re


# Create your views here.

def track_all(request):
    url_all = "https://corona.lmao.ninja/all"
    response = requests.get(url_all, verify=True)
    print(response)
    data = response.json()
    # print(data)
    covid_world.objects.all().delete()
    covid_world(
        total_cases = data['cases'],
        deaths = data['deaths'],
        recovered = data['recovered']
    ).save()
    data = covid_world.objects.all().values('total_cases', 'deaths', 'recovered')
    return render(request, 'index.html', {'queryset': data})