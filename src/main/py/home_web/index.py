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
curs.execute("SELECT names, priority, label, unit FROM sensors ORDER BY priority ASC;")
sensors = curs.fetchall()
oldest_date = 2000000000
sensor_list = "<table style=\"border: .069em solid black;\"><tr><th style=\"padding-left: 1em;padding-right: 2em;\">Capteur</th><th style=\"padding-left: 1em;padding-right: 2em;\">valeur</th><td style=\"padding-left: 1em;padding-right: 2em;\">date</td><td style=\"padding-left: 1em;padding-right: 2em;\"></td></tr>"
for sensor in sensors:
    (sensor_name, priority, sensor_label, unit) = sensor
    if priority<35:
        style_value="font-weight: bold;"
    else:
        style_value=""
    if priority>70:
        style_row=" style=\"color: Silver;\""
    else:
        style_row=""
    curs.execute("SELECT MAX(epochtimestamp), value FROM raw_measures_" + sensor_name + ";")
    last_date_and_value = curs.fetchall()
    (epochdate, value) = last_date_and_value[0]
    if oldest_date>epochdate:
        oldest_date = epochdate
    datestr = time.strftime('%-d/%m/%Y<br/>%H:%M:%S', time.localtime(epochdate))
    sensor_list = sensor_list + "<tr" + style_row + "><td style=\"padding-left: 1em;padding-right: 2em;\">" + sensor_label + "</td><td style=\"text-align: center;padding-left: 1em;padding-right: 2em;" + style_value + "\">" + str(value) + " " + unit + "</td><td style=\"padding-left: 1em;padding-right: 2em;font-size: x-small;text-align: center;\">" + datestr + "</td><td style=\"padding-left: 1em;padding-right: 2em;\"><img src=\"graph.svg\" style=\"width:5em;height:2em;\" /></td></tr>"
sensor_list = sensor_list + "</table>"

if oldest_date != 2000000000:
    datestr = time.strftime('%A %-d %B - %H:%M', time.localtime(oldest_date))
    date_readings = "Relevés le " + datestr + "<br/>"
else:
    date_readings = "Erreur de lecture de date!"
html = """<!DOCTYPE html>
<head>
    <title>Centrale météo St Benoît</title>
</head>
<body>
<h2>Dernières valeurs:</h2>
""" + sensor_list + """
<br/>""" + date_readings + """<br/>
<form action="index.py">
  <input type="submit" style=\"padding: 1em;\" value="Rafraichir" />
</form>
<br/>
</body>
</html>
"""

print(html)
