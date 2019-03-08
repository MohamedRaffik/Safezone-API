import requests
import json
from bs4 import BeautifulSoup

# PRECINCTKey
# Values: 
# - Citywide - all of nyc
# - Brooklyn North / Brooklyn South
# - Bronx
# - Manhattan North / Manhattan South
# - Queens North / Queens South
# - Staten Island
# - By Precinct: [NUM] Precinct (Num is three digits) Ex: 001

# CrimeKey 
# Values: 
# - Murder          
# - Rape
# - Robbery 
# - Fel. Assault.......Felony Assault
# - Burglary  
# - Gr. Larceny........Grand Larceny
# - G.L.A. ............Grand Larceny Auto
# - TotalMajor7........Total of Above Crimes
# - PSB................Patrol
# - Housing
# - Sht. Vic. .........Shooting Victims
# - Sht. Inc. .........Shooting Incidents
# - Rape 1         
# - Petit Larceny
# - Misd. Assault......Misdeamenor Assault
# - Misd. Sex Crimes...Misdeamenor Assault

# RECORDID
# Values: 
# - WTD   Week To Date 
# - 28D   28 Day
# - YTD   Year To Date

# Note: Only values should be changed, not key or label
#       Only one value can be set at a time

URL = 'https://compstat.nypdonline.org/api/reports/13/datasource/list'
filters = {
  'Murder': 'Murder',
  'Rape': 'Rape',
  'Robbery': 'Robbery',
  'Fel. Assault': 'Felony Assault',
  'Burglary': 'Burglary',
  'Gr. Larceny': 'Grand Larceny',
  'G.L.A.': 'Grand Larceny Auto',
  'Sht. Vic.': 'Shooting Victims',
  'Sht. Inc.': 'Shooting Incidents',
  'Rape 1': 'Rape',
  'Petit Larceny': 'Petit Larceny', 
  'Misd. Assault': 'Misdemeanor Assault',
  'Misd. Sex Crimes': 'Misdemeanor Sex Crimes'
}

f = open('crimes.csv', 'w')
f.write('category,crime_date,crime_time,ofns_desc,latitude,longitude')

for filt in filters:
  data = {
    "filters": [
      {
        "key": "PRECINCTKey",    
        "label": "Command",      
        "values": [ "Citywide" ]
      },
      {
        "key": "CrimeKey",
        "label": "Crime",
        "values": [ filt ]
      },
      {
        "key": "RECORDID",
        "label": "Time Period",
        "values": [ "YTD" ]
      }
    ]
  }

  results = requests.post(URL, json=data, verify=False).json()

  # Data returned is a list
  # [
  #   - A single element looks like this
  #   {
  #     "Value": [string] Coordinates ex: '40.7016861,-73.9088377
  #     "Metric": [float] Usually 1.0 
  #     "Title":  [html] Defines the type of crime, date and approximate time of occurrence (nearest hour)
  #                        - Both in Inner HTML of span, in div with class 'text-left'
  #                        - Description Appears in First span and data/time appears in last span
  #     "Color": [string]
  #     "TooltipHtml": [html] Same value as title
  #     "RelatedItems": [List] Usually empty
  #   }
  # ]

  for r in results:
    if r['Title'] == '':
      continue
    f.write('\n{0},{1},{2},{3},{4},{5}'.format(
      filters[filt],
      str(BeautifulSoup(r['Title'], features='html.parser').find_all('span')[-1].string).split(' ')[0],
      str(BeautifulSoup(r['Title'], features='html.parser').find_all('span')[-1].string).split(' ')[-1],
      str(BeautifulSoup(r['Title'], features='html.parser').find_all('span')[0].string),  
      r['Value'].split(',')[0],
      r['Value'].split(',')[-1]
    ))
f.close()


