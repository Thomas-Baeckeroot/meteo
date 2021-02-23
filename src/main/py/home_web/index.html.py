#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import locale
import re
import sys
import time
import traceback
import urllib.parse

import db_module

# from sensors_functions import iso_timestamp

METEO_FOLDER = "/home/pi/meteo/"
CAPTURES_FOLDER = METEO_FOLDER + "captures/"

form = cgi.FieldStorage()
locale.getdefaultlocale()
print("Content-type: text/html; charset=utf-8\n")

html = """<!DOCTYPE html>
<head>
    <title>Centrale météo St Benoît</title>
    <link rel="icon" type="image/svg+xml" href="html/favicon.svg">
</head>
<body style="background-color: lightsteelblue;">"""

two_day_ago = str(db_module.epoch_now() - 172800)

try:
    # Connect or Create DB File
    conn = db_module.get_conn()
    curs = conn.cursor()
    curs.execute(
        "SELECT  sensor, epochtimestamp, measure "
        "FROM    raw_measures AS raw1 "
        "WHERE   epochtimestamp > " + two_day_ago + ""
        "  AND   epochtimestamp ="
        "          ( SELECT  MAX(epochtimestamp)"
        "            FROM    raw_measures AS raw2"
        "            WHERE   epochtimestamp > " + two_day_ago + ""
        "              AND   raw1.sensor = raw2.sensor"
        "            GROUP BY sensor"
        "          ); ")
    values = curs.fetchall()
    last_values = {}
    for value in values:
        (sensor, max_epoch, measure) = value
        last_values[sensor.decode("utf-8")] = (max_epoch, measure)
    # TODO Upper request should be included as LEFT JOIN in below request
    # but when doing so, response took much more time...

    curs.execute(
        "SELECT  name, priority, sensor_label, unit, filepath_data "
        "FROM    sensors"
        "    LEFT JOIN captures ON sensors.name = captures.sensor_name "
        "ORDER BY priority DESC;")
    # SELECT name, priority, sensor_label, unit, epochtimestamp, measure
    # FROM   sensors
    #     LEFT JOIN raw_measures ON sensors.name = raw_measures.sensor
    #     AND epochtimestamp = ( SELECT  MAX(epochtimestamp)  FROM    raw_measures  WHERE   sensor = sensors.name );
    sensors = curs.fetchall()
    oldest_date = -1
    sensor_list =\
        "<table style=\"border: .15em solid black; border-collapse: collapse; background-color: white;\">\n" \
        "<tr style=\"border: .1em solid black; background-color: silver;\">\n" \
        "\t<th style=\"padding-left: 1em; padding-right: 2em;\">Capteur</th>\n" \
        "\t<th style=\"padding-left: 1em; padding-right: 2em;\">valeur</th>\n" \
        "\t<td style=\"padding-left: 1em; padding-right: 2em;\">date</td>\n" \
        "\t<td style=\"padding-left: 1em; padding-right: 2em;\"></td>\n</tr>"
    camera_row = "<tr><td colspan=\"4\"><table style=\"text-align: center;\"><tr>"
    for sensor in sensors:
        (sensor_name, priority, sensor_label, unit, filepath_data) = sensor
        sensor_name = sensor_name.decode('ascii')

        if unit == "picture":  # Below 10, sensors are not displayed in top list (ie: pictures from camera)
            arguments = {'image':filepath_data}
            result = urllib.parse.urlencode(arguments, quote_via=urllib.parse.quote_plus)

            # 'password=xyz&username=administrator'   # "image=" + urllib.parse.quote(filepath_data)
            # "<td><a href=\"capture.html?image=" + urllib.parse.quote(filepath_data) + \
            camera_row = \
                camera_row + \
                "<td><a href=\"capture.html?" + result + \
                "\"><img src=\"captures/" + filepath_data + \
                "\" width=\"360em\" height=\"270em\" style=\"background-color: lightgray\" /></a><br/>" + \
                sensor_label + "<br/>" + re.findall(r"(\d{4}-\d{2}-\d{2}.\d{2}-\d{2})", filepath_data)[0] + "</td>"

        elif priority > 10:
            if priority > 70:
                style_row = "border: .069em solid lightgray;"
                style_value = "font-weight: bold;"
            elif priority < 35:
                style_row = "color: Silver; border: .069em solid lightgray;"
                style_value = ""
            else:
                style_row = "border: .069em solid lightgray;"
                style_value = ""

            sensor_list = sensor_list + "<tr style=\"" + style_row + "\">"
            sensor_list = sensor_list + "\n\t<td style=\"padding-left: 1em;padding-right: 2em;\">" + sensor_label
            if (sensor_name in last_values):
                (epochdate, value) = last_values[sensor_name]
                if oldest_date < epochdate:
                    oldest_date = epochdate
                # locale.getdefaultlocale()
                date_str = time.strftime('%-d/%m/%Y<br/>%H:%M:%S', time.localtime(epochdate))
                sensor_list =\
                    sensor_list + \
                    "</td>\n\t<td style=\"text-align: center;padding-left: 1em;padding-right: 2em;" + \
                    style_value + "\">" + str(value) + " " + unit + "</td>\n" + \
                    "\t<td style=\"padding-left: 1em;padding-right: 2em;font-size: x-small;text-align: center;\">" + \
                    date_str + \
                    "</td>\n\t<td style=\"padding-left: 1em;padding-right: 2em;\">" + \
                    "<a href=\"graph.svg?sensor=" + sensor_name + "&maxepoch=" + str(oldest_date) + \
                    "&width=980\">" + \
                    "<img src=\"graph.svg?sensor=" + sensor_name + "&maxepoch=" + str(oldest_date) + \
                    "&width=100\" style=\"width:100px;height:40px;\" /></a><td></tr>\n"
            else:
                sensor_list = sensor_list + "</td>\n<td style=\"text-align: center;padding-left: 1em;padding-right: 2em;" \
                              + style_value + "\">-</td>\n" \
                              + "<td style=\"padding-left: 1em;padding-right: 2em;font-size: x-small;text-align: center;\">-" \
                              + "</td>\n<td style=\"padding-left: 1em;padding-right: 2em;\"><td></tr>\n"

        # end of 'for sensor in sensors:'

    if oldest_date != -1:
        date_str = time.strftime('%A %-d %B - %H:%M', time.localtime(oldest_date))
        date_readings = "Dernier relevé le " + date_str
    else:
        date_readings = "Erreur de lecture de date!"

    sensor_list = \
        sensor_list + \
        "<tr style=\"border: .15em solid black;\">\n\t<td style=\"padding: 1em;\">" + \
        "<form action=\"index.html\">" + \
        "<input type=\"submit\" style=\"padding: 1.2em;\" value=\"Rafraichir\" />" + \
        "</form></td>\n\t<td colspan=\"3\">" + date_readings + "</td></tr>" + camera_row + \
        "</tr></table></td></tr></table>"

    html = html + "<h3>Dernières valeurs:</h3>" + sensor_list

except Exception as err:
    html = html + "<br/>Exception: {0}<br/>".format(err)
    print("Exception: {0}".format(err), file=sys.stderr)
    traceback.print_exc(file=sys.stderr)

html = html + "</body></html>"
print(html)
