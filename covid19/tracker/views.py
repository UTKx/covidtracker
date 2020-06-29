from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

from .models import covid_world, covid_country

import requests
import json
import ssl
import re
import numpy as np
import pandas as pd

from  .scrape import *

# Create your views here.

def trackCovid(request):
    url_all = "https://corona.lmao.ninja/v2/all"
    response = requests.get(url_all, verify=True)
    data = response.json()

    active = {}
    active_cases = int(data['active'])
    critical = int(data['critical'])
    mild_cases = active_cases - critical
    active['active'] = active_cases
    active['critical'] = critical
    active['mild'] = mild_cases
    print(active)

    closed = {}
    recovered = int(data['recovered'])
    deaths = int(data['deaths'])
    closed_cases = recovered + deaths
    closed['closed'] = closed_cases
    closed['recovered'] = recovered
    closed['deaths'] = deaths
    print(closed)
    
    covid_world.objects.all().delete()
    covid_world(
        total_cases = data['cases'],
        deaths = data['deaths'],
        recovered = data['recovered']
    ).save()
    data = covid_world.objects.all().values('total_cases', 'deaths', 'recovered')
    
    url_country = "https://corona.lmao.ninja/v2/countries"
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
            Critical = datum['critical'],
            Casepermillion = datum['casesPerOneMillion'],
            Deathpermillion = datum['deathsPerOneMillion'],
            Tests = datum['tests'],
            Testpermillion = datum['testsPerOneMillion']
        ).save()
    # print(data)
    data_country_obj = covid_country.objects.all().values('Country', 'Total_Cases', 'Today_Cases', 'Total_Deaths', 'Today_Deaths',
                                                            'Recovered', 'Active', 'Critical', 'Casepermillion', 'Deathpermillion', 'Tests', 'Testpermillion')
    
    json.dumps(list(data_country_obj), cls=DjangoJSONEncoder)

    df = pd.DataFrame(data_country_obj)
    
    df = df.sort_values(['Total_Cases'], ascending=[False])
    df.columns = ['Country, Others', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'Active Cases', 'Critical Cases', 'Cases/ 1M pop', 'Deaths/ 1M pop', 'Total Tests', 'Tests/ 1M pop'] 

    num_format = lambda x: '{:,}'.format(x)
    def build_formatters(df, format):
         return {
             column:format 
             for column, dtype in df.dtypes.items()
             if dtype in [ np.dtype('int64'), np.dtype('float64') ] 
    }
    formatters = build_formatters(df, num_format)

    df = df.to_html(classes="table table-bordered table-hover table-responsive-md", index=False, formatters=formatters)

    return render(request, 'index.html', {'queryset': data, 'html_table': df, 'active': active, 'closed': closed})