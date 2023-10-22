#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import datetime
import logging
import os
import pathlib
import re
import urllib.parse

from db_module import get_home

HOME = get_home()
logging.basicConfig(
    filename= HOME + "/susanoo-web.log",  # = /home/web/susanoo-web.log
    level=logging.DEBUG,
    format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s')
log = logging.getLogger("capture.html.py")

SIZE_LIMIT = 512000  # 500 kiB. Below this value, image is considered without data (mostly black)

BOTTOM_NOTE = """* Les heures sont GMT. Compter +2h en été et +1h en hiver.<br/>"""


def get_picture_from_list_for_time(file_at_hour, hour, minute):
    for i in range(0, 14):
        hour_key = "{:02d}".format(hour) + "-" + "{:02d}".format(minute + i)
        if hour_key in file_at_hour:
            (image_name, image_size) = file_at_hour[str(hour_key)]
            if image_size > SIZE_LIMIT:
                background_color = "Khaki"
            else:
                background_color = "LightBlue"
            return (str("{:02d}".format(minute + i)), image_name, str(background_color))
    return (str("{:02d}".format(minute)), None, str("DarkGray"))


def get_newest_file(folder):
    folder_scan = os.scandir(folder)
    max_mtime = -1
    last_file = ""
    has_daylight_image = False
    # TODO Find somthing better than below to get a "significative" image (ideas: default hour "1000"/"-1" for any last ?
    size_limit = SIZE_LIMIT * 2  # Even if considered "day", an extra value (+50%) is added to get a significative image
    for file_obj in folder_scan:
        name = file_obj.name
        if os.path.isfile(folder + "/" + name):
            mtime = file_obj.stat().st_mtime
            log.debug("Stats from file '{0}': mtime = {1}".format(name, mtime))
            size = file_obj.stat().st_size
            if has_daylight_image:
                if mtime > max_mtime and size > size_limit:
                    log.debug("-> newer daylight file '{0}'".format(name))
                    last_file = name
                    max_mtime = mtime
            else:  # only having night images
                if mtime > max_mtime or size > size_limit:
                    # We got a newer file than the current one... day picture or night?
                    log.debug("-> newer file '{0}' (previous was night)".format(name))
                    last_file = name
                    max_mtime = mtime
                    if size > SIZE_LIMIT:
                        log.debug("   (newer file is a day file)")
                        has_daylight_image = True

    log.debug("Returning most recent file '{0}'".format(last_file))
    return last_file


def get_newest_folder(folder):
    folder_scan = os.scandir(folder)
    max_mtime = -1
    last_folder = ""
    for file_obj in folder_scan:
        name = file_obj.name
        if os.path.isdir(folder + "/" + name):
            mtime = file_obj.stat().st_mtime
            if mtime > max_mtime:
                last_folder = name
                max_mtime = mtime
    log.debug("Returning most recent folder '{0}'".format(last_folder))
    return last_folder


log.info("Starting building a capture page")
print("Content-type: text/html; charset=utf-8\n")
bottom_note = BOTTOM_NOTE

camera = None
year = None
month_day = None
jpeg_image = None
# Read 'image' value from url:
form = cgi.FieldStorage()
image = form.getvalue("image")
# expect something like "grangette/2021/01-10/grangette_2021-01-10Z16-00-07.jpg" or "grangette/2021/01-10/" or "grangette"
log.debug("value image = '{0}'".format(image))

if image:
    # Interpreting values contained in 'image' value from url:
    image_url_split = image.split('/')
    if len(image_url_split) > 3:
        jpeg_image = image_url_split[3]
    if len(image_url_split) > 2:
        month_day = image_url_split[2]
    if len(image_url_split) > 1:
        year = image_url_split[1]
    camera  = image_url_split[0]

    # Validating values:
    if os.path.isfile(HOME + "/captures/" + image):  # <- camera / year / month_day / jpeg_image
        log.debug("Image file is valid: {0}".format(image_url_split))
    
    elif len(image_url_split) > 2 and os.path.isdir(HOME + "/captures/" + camera + "/" + year + "/" + month_day):
        log.debug("Image file is NOT valid but camera, year and month_day are valid.")
        if jpeg_image:
            bottom_note = bottom_note + "/!\\ image " + jpeg_image + " given in parameter is not valid!<br/>"
            jpeg_image = None
    
    elif len(image_url_split) > 1 and os.path.isdir(HOME + "/captures/" + camera + "/" + year):
        log.debug("Values month_day and image are NOT valid but camera and year are valid.")
        bottom_note = bottom_note + "/!\\ image " + str(month_day) + "/" + str(jpeg_image) + " given in parameter is not valid!<br/>"
        month_day = get_newest_folder(HOME + "/captures/" + camera + "/" + year)
        jpeg_image = None

    elif len(image_url_split) > 0 and os.path.isdir(HOME + "/captures/" + camera):
        log.debug("Values year, month_day and image are NOT valid but camera is valid.")
        bottom_note = bottom_note + "/!\\ image " + str(year) + "/" + str(month_day) + "/" + str(jpeg_image) + " given in parameter is not valid!<br/>"
        year = get_newest_folder(HOME + "/captures/" + camera)
        month_day = get_newest_folder(HOME + "/captures/" + camera + "/" + year)
        jpeg_image = None

    else:
        log.debug("Values camera, year, month_day and image are NOT valid.")
        bottom_note = bottom_note + "/!\\ image " + str(camera) + "/" + str(year) + "/" + str(month_day) + "/" + str(jpeg_image) + " given in parameter is not valid!<br/>"
        camera = get_newest_folder(HOME + "/captures")
        year = get_newest_folder(HOME + "/captures/" + camera)
        month_day = get_newest_folder(HOME + "/captures/" + camera + "/" + year)
        jpeg_image = None
        
    log.debug("image -> {0} / {1} / {2} / {3}".format(camera, year, month_day, jpeg_image))
    image_folder = camera + "/" + year + "/" + month_day  # fixme formerly os.path.dirname(pathlib.Path(...)

else:  # no 'image' value given in url
    log.debug("No image value found => will pick first folder in capture")
    capture_folder_scan = os.scandir(HOME + "/captures")
    camera = get_newest_folder(HOME + "/captures")
    year = get_newest_folder(HOME + "/captures/" + camera)
    month_day = get_newest_folder(HOME + "/captures/" + camera + "/" + year)
    jpeg_image = None    

if not jpeg_image:
    jpeg_image = get_newest_file(HOME + "/captures/" + camera + "/" + year + "/" + month_day)

folder = HOME + "/captures/" + camera + "/" + year + "/" + month_day
folder_scan = os.scandir(folder)
file_at_hour = {}
size_at_hour = {}
for file_obj in folder_scan:
    name = file_obj.name
    size = file_obj.stat().st_size
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
    <td colspan="2"><a href="index.html">accueil</a></td> <!-- style="border: none; background-color: transparent;" -->
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">0h/12h*</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">1h</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">2h</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">3h</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">4h</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">5h</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">6h</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">7h</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">8h</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">9h</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">10h</th>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">11h</th>
    <td>-</td>
</tr>"""

for meridiem in ["am", "pm"]:
    html = html \
           + "<tr style=\"font-size: small;\">" \
           + "<td>&lt;</td>" \
           + "<td style=\"font-size: medium; border: .02em solid black; background-color: whitesmoke;\">" \
           + meridiem + "</td>"

    for h_num in range(0, 12):
        if meridiem == "am":
            hour = h_num
        else:
            hour = h_num + 12

        for minute in [0, 15, 30, 45]:
            (min_str, image_name, background_color) = get_picture_from_list_for_time(file_at_hour, hour, minute)
            if image_name:
                arguments = {'image': camera + "/" + year + "/" + month_day + "/" + image_name}
                result = urllib.parse.urlencode(arguments, quote_via=urllib.parse.quote_plus)
                html = html + "<td style=\"background-color: " + background_color + ";\"><a href=\"capture.html?" + \
                       result + "\"><div style=\"height:100%;width:100%\">" + min_str + "</div></a></td>"
            else:  # image_name is None => no pictures for this quater of an hour
                html = html + "<td style=\"background-color: " + background_color + ";\">" + min_str + "</td>"
                # style=\"height:100%;width:100%\"

    html = html + "<td>&gt;</td></tr>"

html = html + """</table>
<img src=\"captures/""" + camera + "/" + year + "/" + month_day + "/" + str(jpeg_image) + """\" style=\"width: 60em; height: 45em\" /><br/><br/>
Nom de l'appareil: <a style="font-family: monospace">""" + camera + """</a>&nbsp;&nbsp;&nbsp;&nbsp;
""" + str(jpeg_image) + """
<br/>
<p>""" + bottom_note + """
</p>
  </body>
</html>"""

print(html)
log.info("Terminated building a capture page")
