# import urllib.request
# import urllib.parse
# import urllib.error
# from bs4 import BeautifulSoup
# import ssl
# import json

# from urllib.request import Request, urlopen

# from .models import active_cases, closed_cases

# url = 'https://www.worldometers.info/coronavirus/'
# req = Request(url, headers= {'User-Agent' : 'Chrome/80.0.3987.149'})
# page = urlopen(req).read()

# soup = BeautifulSoup(page, 'html.parser')
# html = soup.prettify('utf-8')

# active = {}
# active['infected'] = []
# active['mild'] = []
# active['critical'] = []

# for divs in soup.find('div', attrs = {'class' : 'number-table-main'}):
#     active['infected'] = divs

# astr = active['infected']
# # print(astr)
# anum = int(astr.replace(',', ''))
# # print(anum, type(anum))

# active['infected'] = anum
# active['mild'] = int(anum * 0.95)
# active['critical'] = int(anum * 0.05)
# # print(active)

  
# # active_cases.objects.all().delete()
# # active_cases(
#     # active_cases = active['infected'],
#     # mild_cases = active['mild'],
#     # critical_cases = active['critical']
# # ).save()
# # active = active_cases.objects.all().values('active_cases', 'mild_cases', 'critical_cases')