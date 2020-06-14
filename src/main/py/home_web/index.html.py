#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import psycopg2  # ProgreSQL library
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
conn = psycopg2.connect(database="meteo")  # Connect to PostgreSQL DB
curs = conn.cursor()
curs.execute("SELECT name, priority, sensor_label, unit FROM sensors ORDER BY priority ASC;")
sensors = curs.fetchall()
oldest_date = -1
sensor_list = "<table style=\"border: .069em solid black;\">" \
              "<tr><th style=\"padding-left: 1em;padding-right: 2em;\">Capteur</th>" \
              "<th style=\"padding-left: 1em;padding-right: 2em;\">valeur</th>" \
              "<td style=\"padding-left: 1em;padding-right: 2em;\">date</td>" \
              "<td style=\"padding-left: 1em;padding-right: 2em;\"></td></tr>"
for sensor in sensors:
    (sensor_name, priority, sensor_label, unit) = sensor
    if priority < 35:
        style_value = "font-weight: bold;"
    else:
        style_value = ""
    if priority > 70:
        style_row = " style=\"color: Silver;\""
    else:
        style_row = ""

    curs.execute("""
        SELECT  epochtimestamp, measure
        FROM    raw_measures 
        WHERE   sensor = '""" + sensor_name + """'
          AND   epochtimestamp = (  SELECT  MAX(epochtimestamp) 
                                    FROM    raw_measures 
                                    WHERE   sensor = '""" + sensor_name + """' );""" )
    last_date_and_value = curs.fetchall()

    sensor_list = sensor_list + "<tr" + style_row + ">"
    sensor_list = sensor_list + "<td style=\"padding-left: 1em;padding-right: 2em;\">"\
                  + sensor_label
    if len(last_date_and_value) > 0:
        (epochdate, value) = last_date_and_value[0]
        if oldest_date < epochdate:
            oldest_date = epochdate
        # locale.getdefaultlocale()
        date_str = time.strftime('%-d/%m/%Y<br/>%H:%M:%S', time.localtime(epochdate))
        sensor_list = sensor_list + \
                      "</td>\n<td style=\"text-align: center;padding-left: 1em;padding-right: 2em;" \
                      + style_value + "\">" + str(value) + " " + unit + "</td>\n" \
                      "<td style=\"padding-left: 1em;padding-right: 2em;font-size: x-small;text-align: center;\">" \
                      + date_str \
                      + "</td>\n<td style=\"padding-left: 1em;padding-right: 2em;\">" \
                      + "<a href=\"graph.svg?sensor=" + sensor_name + "&maxepoch=" + str(oldest_date)\
                      + "&width=980\">" \
                      + "<img src=\"graph.svg?sensor=" + sensor_name + "&maxepoch=" + str(oldest_date) \
                      + "&width=100\" style=\"width:100px;height:40px;\" /></a><td></tr>\n"
    else:
        sensor_list = sensor_list + "</td>\n<td style=\"text-align: center;padding-left: 1em;padding-right: 2em;" \
                      + style_value + "\">-</td>\n" \
                      + "<td style=\"padding-left: 1em;padding-right: 2em;font-size: x-small;text-align: center;\">-" \
                      + "</td>\n<td style=\"padding-left: 1em;padding-right: 2em;\"><td></tr>\n"

sensor_list = sensor_list + "</table>"

if oldest_date != -1:
    date_str = time.strftime('%A %-d %B - %H:%M', time.localtime(oldest_date))
    date_readings = "Dernier relevé le " + date_str + "<br/>"
else:
    date_readings = "Erreur de lecture de date!"
html = """<!DOCTYPE html>
<head>
    <title>Centrale météo St Benoît</title>
</head>
<body>
<h2>Dernières valeurs:</h2>
""" + sensor_list + """<br/>
""" + date_readings + """<br/>
<form action="index.html">
  <input type="submit" style=\"padding: 1.2em;\" value="Rafraichir" />
</form>
<br/>
</body>
</html>"""

print(html)
