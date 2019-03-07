import requests
import csv
import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres', password='Milbucks97')
cur = conn.cursor()

station_request = requests.get('https://data.cityofnewyork.us/api/views/kk4q-3rt2/rows.csv?accessType=DOWNLOAD').text.split('\n')

cur.execute('drop table if exists subway_stations')
cur.execute('create table subway_stations(url text, id int primary key, name text, line text, notes text, latitude float, longitude float)')
count = 0
for line in csv.DictReader(station_request):
  if count > 50: break
  else: count += 1
  coordinates = [ float(coord) for coord in line['the_geom'][line['the_geom'].index('(') + 1 : line['the_geom'].index(')')].split(' ')[::-1] ]
  line['Latitude'] = coordinates[0]
  line['Longitude'] = coordinates[1]
  line.pop('the_geom', None)
  data = [ line['URL'], line['OBJECTID'], line['NAME'], line['LINE'], line['NOTES'], line['Latitude'], line['Longitude'] ]
  cur.execute('insert into subway_stations(url, id, name, line, notes, latitude, longitude) values (%s, %s, %s, %s, %s, %s, %s)', data)

crime_request = requests.get('https://data.cityofnewyork.us/api/views/uip8-fykc/rows.csv?accessType=DOWNLOAD').text.split('\n')

cur.execute('drop table if exists crime_info')
cur.execute('create table crime_info(arrest_key int primary key, arrest_date Date, pd_cd int, pd_desc text, ky_cd int, ofns_desc text, law_code text, law_cat_cd text, arrest_precinct text, latitude float, longitude float)')
count = 0
for line in csv.DictReader(crime_request):
  if count > 50: break
  else: count += 1
  if line['PD_CD'] == '': line['PD_CD'] = 0
  if line['KY_CD'] == '': line['KY_CD'] = 0
  if line['LAW_CAT_CD'] == '': line['LAW_CAT_CD'] = 0
  data = [ line['ARREST_KEY'], line['ARREST_DATE'], line['PD_CD'], line['PD_DESC'], line['KY_CD'], line['OFNS_DESC'], line['LAW_CODE'], line['LAW_CAT_CD'], line['ARREST_PRECINCT'], line['Latitude'], line['Longitude'] ]
  cur.execute('insert into crime_info(arrest_key, arrest_date, pd_cd, pd_desc, ky_cd, ofns_desc, law_code, law_cat_cd, arrest_precinct, latitude, longitude) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)

conn.commit()
conn.close()