from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder

from .models import CovidWorld, CovidCountry

import requests
import json
import ssl
import re
import numpy as np
import pandas as pd


def trackCovid(request):
    # URL for world stats
    url_all = "https://corona.lmao.ninja/v2/all"
    response = requests.get(url_all, verify=True)

    # Converting to json format
    data = response.json()

    # Dictionary for active cases
    active = {}
    active_cases = int(data['active'])
    critical = int(data['critical'])
    mild_cases = active_cases - critical
    active['active'] = active_cases
    active['critical'] = critical
    active['mild'] = mild_cases
    active['mild_per'] = round((mild_cases/active_cases)*100)
    active['crit_per'] = round((critical/active_cases)*100)

    # Dictionary for closed cases
    closed = {}
    recovered = int(data['recovered'])
    deaths = int(data['deaths'])
    closed_cases = recovered + deaths
    closed['closed'] = closed_cases
    closed['recovered'] = recovered
    closed['deaths'] = deaths
    closed['rec_per'] = round((recovered/closed_cases)*100)
    closed['death_per'] = round((deaths/closed_cases)*100)

    # Deleting the rows in the table
    CovidWorld.objects.all().delete()
    
    # Inserting the data in table
    CovidWorld(
        total_cases=data['cases'],
        deaths=data['deaths'],
        recovered=data['recovered']
    ).save()
    
    # Fethching values from the table
    data = CovidWorld.objects.all().values('total_cases', 'deaths', 'recovered')

    # URL for country stats
    url_country = "https://corona.lmao.ninja/v2/countries"
    response = requests.get(url_country, verify=True)
    
    # Converting to json format
    data_country = response.json()

    # Deleting the rows in the table
    CovidCountry.objects.all().delete()
    
    # Inserting the data in table in loop
    for datum in data_country:
        CovidCountry(
            country=datum['country'],
            total_cases=datum['cases'],
            today_cases=datum['todayCases'],
            total_deaths=datum['deaths'],
            today_deaths=datum['todayDeaths'],
            recovered=datum['recovered'],
            active=datum['active'],
            critical=datum['critical'],
            casepermillion=datum['casesPerOneMillion'],
            deathpermillion=datum['deathsPerOneMillion'],
            tests=datum['tests'],
            testpermillion=datum['testsPerOneMillion']
        ).save()

    # Fethching values from the table
    data_country_obj = CovidCountry.objects.all().values('country', 'total_cases', 'today_cases', 'total_deaths', 'today_deaths',
                                                         'recovered', 'active', 'critical', 'casepermillion', 'deathpermillion', 'tests', 'testpermillion')

    # Converting the passed object to json format
    json.dumps(list(data_country_obj), cls=DjangoJSONEncoder)

    # Converting the object to dataframe
    df = pd.DataFrame(data_country_obj)

    # Sorting the dataframe in descending order by total cases
    df = df.sort_values(['total_cases'], ascending=[False])
    
    # Passing the new values to the dataframe columns
    df.columns = ['Country, Others', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered',
                  'Active Cases', 'Critical Cases', 'Cases/ 1M pop', 'Deaths/ 1M pop', 'Total Tests', 'Tests/ 1M pop']

    # Formatting the dataframe data by adding ',' to the values
    def num_format(x): return '{:,}'.format(x)

    def build_formatters(df, format):
        return {
            column: format
            for column, dtype in df.dtypes.items()
            if dtype in [np.dtype('int64'), np.dtype('float64')]
        }
    formatters = build_formatters(df, num_format)

    # Converting dataframe to html table format
    df = df.to_html(classes="table table-bordered table-hover table-responsive-md sticky",
                    index=False, formatters=formatters)

    return render(request, 'index.html', {'queryset': data, 'html_table': df, 'active': active, 'closed': closed})


def searchByCountry(request):
    # URL for world stats
    url_all = "https://corona.lmao.ninja/v2/all"
    response = requests.get(url_all, verify=True)

    # Converting to json format
    data = response.json()

    # Dictionary for active cases
    active = {}
    active_cases = int(data['active'])
    critical = int(data['critical'])
    mild_cases = active_cases - critical
    active['active'] = active_cases
    active['critical'] = critical
    active['mild'] = mild_cases
    active['mild_per'] = round((mild_cases/active_cases)*100)
    active['crit_per'] = round((critical/active_cases)*100)

    # Dictionary for closed cases
    closed = {}
    recovered = int(data['recovered'])
    deaths = int(data['deaths'])
    closed_cases = recovered + deaths
    closed['closed'] = closed_cases
    closed['recovered'] = recovered
    closed['deaths'] = deaths
    closed['rec_per'] = round((recovered/closed_cases)*100)
    closed['death_per'] = round((deaths/closed_cases)*100)

    # Fethching values from the table
    data = CovidWorld.objects.all()

    # Geting data from get request
    get_data = request.GET.get('search')

    # Querying data 
    query = CovidCountry.objects.filter(country__istartswith=get_data).values('country', 'total_cases', 'today_cases', 'total_deaths', 'today_deaths',
                                                                              'recovered', 'active', 'critical', 'casepermillion', 'deathpermillion', 'tests', 'testpermillion')
    
    # Converting the passed object to json format
    json.dumps(list(query), cls=DjangoJSONEncoder)

    # Converting the object to dataframe
    df = pd.DataFrame(query)
    
    # Sorting the dataframe in descending order by total cases
    df = df.sort_values(['total_cases'], ascending=[False])

    # Passing the new values to the dataframe columns
    df.columns = ['Country, Others', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered',
                  'Active Cases', 'Critical Cases', 'Cases/ 1M pop', 'Deaths/ 1M pop', 'Total Tests', 'Tests/ 1M pop']
    
    # Formatting the dataframe data by adding ',' to the values
    def num_format(x): return '{:,}'.format(x)

    def build_formatters(df, format):
        return {
            column: format
            for column, dtype in df.dtypes.items()
            if dtype in [np.dtype('int64'), np.dtype('float64')]
        }
    formatters = build_formatters(df, num_format)

    # Converting dataframe to html table format
    df = df.to_html(classes="table table-bordered table-hover table-responsive-md sticky",
                    index=False, formatters=formatters)

    return render(request, 'search.html', {'html_table': df, 'queryset': data, 'active': active, 'closed': closed})
