import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json

from urllib.request import Request, urlopen

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
    # active_cases['mild'] = int(active_cases['infected']) * .95
    # active_cases['critical'] = int(active_cases['infected']) * .05
print(active_cases)

def add():
    a =5
    b =4
    c=a+b
    return c

def sdf(c):
    return c*10