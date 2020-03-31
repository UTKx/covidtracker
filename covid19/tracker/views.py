from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

from .models import *

import certifi
import requests
import json
import ssl
import re

from  .scrape import *

# Create your views here.


def track_all(request):
    url_all = "https://corona.lmao.ninja/all"
    response = requests.get(url_all, verify='/etc/ssl/certs/ca-certificates.crt')
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
    
    active_cases.objects.all().delete()
    active_cases(
        active_cases = active_cases['infected'],
        mild_cases = active_cases['mild'],
        critical_cases = active_cases['critical']
    ).save()
    active = active_cases.objects.all().values('active_cases', 'mild_cases', 'critical_cases')
    return render(request, 'index.html', {'queryset': data}, {'active_cases': active_cases})