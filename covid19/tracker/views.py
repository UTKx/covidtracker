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


def track_all(request):
    url_all = "https://corona.lmao.ninja/all"
    response = requests.get(url_all, verify='/etc/ssl/certs/ca-certificates.crt')
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
    response = requests.get(url_country, verify='/etc/ssl/certs/ca-certificates.crt')
    data_country = response.json()

    covid_country.objects.all().delete()
    for datum in data_country:
        covid_country(
            country_name = datum['country'],
            total_cases = datum['cases'],
            today_cases = datum['todayCases'],
            total_deaths = datum['deaths'],
            today_deaths = datum['todayDeaths'],
            recovered = datum['recovered'],
            active = datum['active'],
            critical = datum['critical']
        ).save()
    print(data)
    data_country_obj = covid_country.objects.all().values('country_name', 'total_cases', 'today_cases', 'total_deaths', 'today_deaths',
                                                            'recovered', 'active', 'critical')
    
    json.dumps(list(data_country_obj), cls=DjangoJSONEncoder)

    df = pd.DataFrame(data_country_obj)
    df.fillna('', inplace=True)
    df = df.to_html(classes="table table-light table-bordered table-hover my-table")
    # df1 = re.sub(r'<table border="1"', r'<table', df)

    return render(request, 'index.html', {'queryset': data, 'html_table': df})