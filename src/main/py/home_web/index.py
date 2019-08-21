#!/usr/bin/python3
# coding: utf-8

import cgi
import sqlite3

# from sensors_functions import iso_timestamp

METEO_FOLDER = "/home/pi/meteo/"
DB_NAME = METEO_FOLDER + "meteo.db"
CAPTURES_FOLDER = METEO_FOLDER + "captures/"

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

# Connect or Create DB File
conn = sqlite3.connect(DB_NAME)
curs = conn.cursor()
curs.execute("SELECT names, unit FROM sensors;")
sensors = curs.fetchall()
sensor_list = "<table><tr><th>Capteur</th><th>valeur</th></tr>"
for sensor in sensors:
    (sensor_name, unit) = sensor
    curs.execute("SELECT MAX(epochtimestamp), value FROM raw_measures_" + sensor_name + ";")
    last_date_and_value = curs.fetchall()
    
    sensor_list = sensor_list + "<tr><td>" + sensor_name + "</td><td>" + str(last_date_and_value) + unit + " (date)</td></tr>"
sensor_list = sensor_list + "</table>"

html = """<!DOCTYPE html>
<head>
    <title>Centrale météo St Benoît</title>
</head>
<body>
<h2>Dernières valeurs:</h2>
""" + sensor_list + """
<br/>
</body>
</html>
"""

print(html)
