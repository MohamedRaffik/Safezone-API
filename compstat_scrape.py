from requests import post
import json
from bs4 import BeautifulSoup
from os import getenv

from psycopg2 import connect

conn = connect(dbname='postgres', user='postgres', password='Milbucks97')
cur = conn.cursor()

cur.execute('drop table if exists crime_compstat')
cur.execute('create table crime_compstat(category_id int, crime_date date, ofns_desc text, pd_desc text, latitude float, longitude float)')

categories = {
  1: [ 'Murder', 'MURDER & NON-NEGL. MANSLAUGHTE' ],
  2: [ 'Rape', 'RAPE', 'FORCIBLE TOUCHING' ],
  3: [ 'Robbery', 'ROBBERY' ],
  4: [ 'Felony Assault', 'FELONY ASSAULT' ],
  5: [ 'Burglary', 'BURGLARY' ],
  6: [ 'Grand Larceny', 'GRAND LARCENY' ],
  7: [ 'Petit Larceny', 'PETIT LARCENY', 'POSSESSION OF STOLEN PROPERTY', 'OTHER OFFENSES RELATED TO THEFT' ],
  8: [ 'Misdemeanor Assault', 'ASSAULT 3 & RELATED OFFENSES', 'OFFENSES AGAINST THE PERSON' ],
  9: [ 'Misdemeanor Sex Crimes', 'SEX CRIMES', 'PROSTITUTION & RELATED OFFENSES' ],
  10: [ 'KIDNAPPING', 'KIDNAPPING & RELATED OFFENSES' ],
  11: [ 'OFF. AGNST PUB ORD SENSBLTY &', 'LOITERING FOR DRUG PURPOSES', 'OFF. AGNST PUB ORD SENSBLTY & RGHTS TO PRIV', 'DISORDERLY CONDUCT', 'DANGEROUS WEAPONS', 'DANGEROUS DRUGS', 'INTOXICATED AND IMPAIRED DRIVING', 'INTOXICATED/IMPAIRED DRIVING', 'HARRASSMENT 2' ],
  12: [ 'Shooting Victims', 'Shooting Incidents' ]
}


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
  # 'G.L.A.': 'Grand Larceny Auto',
  'Sht. Vic.': 'Shootings',
  'Sht. Inc.': 'Shootings',
  'Rape 1': 'Rape',
  'Petit Larceny': 'Petit Larceny', 
  'Misd. Assault': 'Misdemeanor Assault',
  'Misd. Sex Crimes': 'Misdemeanor Sex Crimes'
}


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

  results = post(URL, json=data, verify=False).json()

  # Data returned is a list
  # [
  #   - A single element looks like this
  #   {
  #     "Value": [string] Coordinates ex: '40.7016861,-73.9088377
  #     "Metric": [float] Usually 1.0 
  #     "Title":  [html] Defines the type of crime, date and approximate time of occurrence (nearest hour)
  #                        - Both in Inner HTML of span, in div with class 'text-left'
  #                        - Description Appears in First span in title or in the innerHTML and data/time appears in last span
  #     "Color": [string]
  #     "TooltipHtml": [html] Same value as title
  #     "RelatedItems": [List] Usually empty
  #   }
  # ]

  for r in results:
    if r['Title'] == '':
      continue
    crime_date = str(BeautifulSoup(r['Title'], features='html.parser').find_all('span')[-1].string).split(' ')[0]
    ofns_desc = filters[filt]
    pd_desc = BeautifulSoup(r['Title'], features='html.parser').find_all('span')[0]
    latitude = r['Value'].split(',')[0]
    longitude = r['Value'].split(',')[-1]
    category = 0
    for i in categories: 
      if ofns_desc in categories[i]: 
        category = i
        break
    data = [ category, crime_date, ofns_desc, pd_desc.attrs.get('title') if pd_desc.attrs.get('title') != None else str(pd_desc.string), latitude, longitude ]
    cur.execute('insert into crime_compstat(category_id, crime_date, ofns_desc, pd_desc, latitude, longitude) values (%s, %s, %s, %s, %s, %s)', data)

conn.commit()
conn.close()


