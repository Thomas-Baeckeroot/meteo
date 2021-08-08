#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import os
import pathlib
import re
import urllib.parse

from db_module import get_home

METEO_FOLDER = "/home/pi/meteo/"
CAPTURES_FOLDER = METEO_FOLDER + "captures/"
data_limit = 512000  # 500 kiB. Below this value, image is considered without data (mostly black)

print("Content-type: text/html; charset=utf-8\n")
form = cgi.FieldStorage()
image = form.getvalue("image")
# image="grangette/2021/01-10/grangette_2021-01-10Z16-00-07.jpg"

image_folder = os.path.dirname(pathlib.Path(image))
folder = get_home() + "/captures/" + image_folder
folder_scan = os.scandir(folder)
file_at_hour = {}
size_at_hour = {}
for file in folder_scan:
    name = file.name
    size = file.stat().st_size
    hour_key = re.findall(r"\d{4}-\d{2}-\d{2}.(\d{2}-\d{2})", name)[0]
    file_at_hour[str(hour_key)] = (name, size)

html = """<!DOCTYPE html>
<html>
  <head>
    <title>Centrale météo St Benoît</title>
    <link rel="icon" type="image/svg+xml" href="html/favicon.svg">
    <style>
        table, th {
          border-collapse: collapse; border: none;
        }
        td {
          text-align: center;
        }
        A {text-decoration: none;}
    </style>
  </head>
  <body style="background-color: lightsteelblue;">
<table style="width: 60em; height:4.3em;"> <!-- border: .02em solid black -->
<tr style="text-align: left;">
    <td><a href="index.html">index</a></td> <!-- style="border: none; background-color: transparent;" -->
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">0h / 12h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">1h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">2h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">3h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">4h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">5h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">6h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">7h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">8h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">9h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">10h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">11h</td>"""

for meridiem in ["am", "pm"]:
    html = html \
           + "</tr><tr style=\"font-size: small;\">" \
           + "<td style=\"font-size: medium; border: .02em solid black; background-color: whitesmoke;\">" \
           + meridiem + "</td>"

    for h_num in range(0, 12):
        if meridiem == "am":
            hour = h_num
        else:
            hour = h_num + 12

        for minute in ["00", "15", "30", "45"]:
            hour_key = "{:02d}".format(hour) + "-" + minute
            if hour_key in file_at_hour:
                (image_name, image_size) = file_at_hour[str(hour_key)]
                arguments = {'image':image_folder + "/" + image_name}
                result = urllib.parse.urlencode(arguments, quote_via=urllib.parse.quote_plus)
                if image_size > data_limit:
                    cell_style = " style=\"background-color: Khaki;\""
                else:
                    cell_style = " style=\"background-color: LightBlue;\""
                html = html + "<td" + cell_style + "><a href=\"capture.html?" + result + \
                        "\"><div style=\"height:100%;width:100%\">" + minute + "</div></a></td>"
            else:
                html = html + "<td style=\"background-color: DarkGray;\">" + minute + "</td>"
                # style=\"height:100%;width:100%\"

html = html + """</tr>
</table>
<img src=\"captures/""" + image + """\" style=\"width: 60em\" />
  </body>
</html>"""

print(html)
