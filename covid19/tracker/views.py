from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

from .models import *

import requests
import json
import ssl
import re
import pandas as pd

from  .scrape import *

# Create your views here.

def track(request):
    url_all = "https://corona.lmao.ninja/all"
    response = requests.get(url_all, verify=True)
    print(response)
    data = response.json()
    
    covid_world.objects.all().delete()
    covid_world(
        total_cases = data['cases'],
        deaths = data['deaths'],
        recovered = data['recovered']
    ).save()
    data = covid_world.objects.all().values('total_cases', 'deaths', 'recovered')
    
    url_country = "https://corona.lmao.ninja/countries"
    response = requests.get(url_country, verify=True)
    data_country = response.json()

    covid_country.objects.all().delete()
    for datum in data_country:
        covid_country(
            Country = datum['country'],
            Total_Cases = datum['cases'],
            Today_Cases = datum['todayCases'],
            Total_Deaths = datum['deaths'],
            Today_Deaths = datum['todayDeaths'],
            Recovered = datum['recovered'],
            Active = datum['active'],
            Critical = datum['critical']
        ).save()
    print(data)
    data_country_obj = covid_country.objects.all().values('Country', 'Total_Cases', 'Today_Cases', 'Total_Deaths', 'Today_Deaths',
                                                            'Recovered', 'Active', 'Critical')
    
    json.dumps(list(data_country_obj), cls=DjangoJSONEncoder)

    df = pd.DataFrame(data_country_obj)
    df = df.to_html(classes="table table-striped table-bordered table-hover table-responsive-md")

    return render(request, 'index.html', {'queryset': data, 'html_table': df})