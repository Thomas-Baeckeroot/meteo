#!/usr/bin/python3
# coding: utf-8

import cgi
import sqlite3
import time
import locale

# from sensors_functions import iso_timestamp

METEO_FOLDER = "/home/pi/meteo/"
DB_NAME = METEO_FOLDER + "meteo.db"
CAPTURES_FOLDER = METEO_FOLDER + "captures/"

form = cgi.FieldStorage()
locale.getdefaultlocale()
print("Content-type: text/html; charset=utf-8\n")

# Connect or Create DB File
conn = sqlite3.connect(DB_NAME)
curs = conn.cursor()
curs.execute("SELECT names, unit FROM sensors;")
sensors = curs.fetchall()
sensor_list = "<table width=\"90%\"><tr><th>Capteur</th><th>valeur</th></tr>"
for sensor in sensors:
    (sensor_name, unit) = sensor
    curs.execute("SELECT MAX(epochtimestamp), value FROM raw_measures_" + sensor_name + ";")
    last_date_and_value = curs.fetchall()
    (epochdate, value) = last_date_and_value[0]
    datestr = time.strftime('%A %-d %b. - %H:%M<small>:%S</small>', time.localtime(epochdate))
    sensor_list = sensor_list + "<tr><td>" + sensor_name + "</td><td>" + str(value) + " " + unit + "</td><td>" + datestr + "</td><td><img src=\"graph.svg\" style=\"width:80px;height:22px;\" /></td></tr>"
sensor_list = sensor_list + "</table>"

html = """<!DOCTYPE html>
<head>
    <title>Centrale météo St Benoît</title>
</head>
<body>
<h2>Dernières valeurs:</h2>
""" + sensor_list + """
<br/>
<form action="index.py">
  <input type="submit" value="Rafraichir" />
</form>
<br/>
</body>
</html>
"""

print(html)
