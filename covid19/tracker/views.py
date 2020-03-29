from django.shortcuts import render

import requests
import json

# Create your views here.

def track_all(request):
    url_all = "https://corona.lmao.ninja/all"
    response = request.GET(url_all, verify=CERT_REQUIRED)
    data = response.json()
    print(data)
    return render(request, 'index.html')