import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json

from urllib.request import Request, urlopen

from .models import active_cases, closed_cases

url = 'https://www.worldometers.info/coronavirus/'
req = Request(url, headers= {'User-Agent' : 'Chrome/80.0.3987.149'})
page = urlopen(req).read()

soup = BeautifulSoup(page, 'html.parser')
html = soup.prettify('utf-8')

active_cases = {}
active_cases['infected'] = []
active_cases['mild'] = []
active_cases['critical'] = []

for divs in soup.find('div', attrs = {'class' : 'number-table-main'}):
    active_cases['infected'] = divs
    # print(active_cases['infected'])

astr = active_cases['infected']
# print(astr)
anum = int(astr.replace(',', ''))
# print(anum, type(anum))

active_cases['infected'] = anum
active_cases['mild'] = int(anum * 0.95)
active_cases['critical'] = int(anum * 0.05)
# print(active_cases)

