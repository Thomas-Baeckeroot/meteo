#!/usr/bin/python3
# coding: utf-8

"""
Serves SVG chart of requested sensor.
"""

import cgi
# import os

# from svg.charts.plot import Plot
# from svg.charts import bar
# from svg.charts import time_series
# from svg.charts import pie
# from svg.charts import schedule
from svg.charts import line

import sqlite3
# import time


SECONDS_IN_ONE_DAY = 86400
METEO_FOLDER = "/home/pi/meteo/"
DB_NAME = METEO_FOLDER + "meteo.db"
CAPTURES_FOLDER = METEO_FOLDER + "captures/"
# START_TIME = time.time()


def generate_samples():
    yield 'Line', sample_Line()


def sample_Line():
    form = cgi.FieldStorage()
    sensor_name = form.getvalue("sensor")

    width = form.getvalue("width")
    if width is None:
        width = 500.
        # Measured widths: phones=980, Mc=1440
    else:
        width = float(width)
    height = width * 2. / 5.
    scale_hours = int(2700. / width)

    maxepoch = form.getvalue("maxepoch")
    if maxepoch is None:
        maxepoch = 2000000000
    maxepoch = int(maxepoch)
    
    minepoch = maxepoch - SECONDS_IN_ONE_DAY

    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    curs.execute("SELECT epochtimestamp, value FROM raw_measures_" + sensor_name + " WHERE epochtimestamp<" + str(maxepoch) + " AND epochtimestamp>" + str(minepoch) + ";")

    date_and_value = curs.fetchall()
    epochdates = list()
    values = list()
    for i in list(range(len(date_and_value))):
        epoch = date_and_value[i][0]
        epoch_minutes = round(epoch/60.)
        if (epoch_minutes % (60 * scale_hours)) == 0:
            epoch_hours = epoch_minutes / 60
            hour_in_day = int(epoch_hours % 24)
            epochdates.append(str(hour_in_day) + ":00")
        else:
            epochdates.append('')
        # epochdates.append(date_and_value[i][0])
        values.append(date_and_value[i][1])

    g = line.Line()
    options = dict(
        scale_integers=True,
        area_fill=True,
        width=int(width),  # calculations done with width and height, must be integer in pixel ('em' not accepted...)
        height=int(height),
        fields=epochdates,
        # fields=['18:00', '', '0:00', '', '6:00', '', '12:00', '', '18:00'],
        graph_title='Question 7',
        show_graph_title=False,
        no_css=False,
    )
    g.__dict__.update(options)
    # g.add_data({'data': [-2, 3, 1, 3, 1], 'title': 'Female'})  # , 'title': 'Female'
    # g.add_data({'data': [11, 10, 9, 9, 9, 9, 10, 11, 14], 'title': 'Temperature'})  # , 'title': 'Female'
    g.add_data({'data': values, 'title': ''})
    # g.add_data({'data': [11.6, 10.4, 9.6, 9.0, 9.3, 9.7, 10.3, 11.7, 14.0], 'title': ''})
    # g.add_data({'data': [0, 2, 1, 5, 4], 'title': 'Male'})
    return g


def gen_sample():
    yield sample_Line()


def save_samples():
    # root = os.path.dirname(__file__)
    for sample_name, sample in generate_samples():
    # sample = gen_sample()

        res = sample.burn()
        print(res)


if __name__ == '__main__':
    print("Content-type: text/html; charset=utf-8\n")
    print("""<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">""")
    save_samples()
