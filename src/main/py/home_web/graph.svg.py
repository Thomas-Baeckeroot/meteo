#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Serves SVG chart of requested sensor.
"""

import cgi

import db_module
import logging

from svg.charts import line

logging.basicConfig(
    filename=db_module.get_home() + "/susanoo-web.log",  # = /home/pi/susanoo-web.log
    level=logging.DEBUG,
    format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s')
log = logging.getLogger("graph.svg.py")

SECONDS_IN_ONE_DAY = 86400
METEO_FOLDER = "/home/pi/meteo/"
CAPTURES_FOLDER = METEO_FOLDER + "captures/"


# START_TIME = time.time()


def generate_samples():
    yield 'Line', sample_line()


def sample_line():
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

    if width < 350:
        tiny_graph = True
    else:
        tiny_graph = False

    maxepoch = form.getvalue("maxepoch")
    if maxepoch is None:
        maxepoch = 2000000000
    maxepoch = int(maxepoch)

    minepoch = maxepoch - SECONDS_IN_ONE_DAY

    conn = db_module.get_conn()
    curs = conn.cursor()
    curs.execute("  SELECT  epochtimestamp, measure"
                 "  FROM    raw_measures"
                 "  WHERE   epochtimestamp<" + str(maxepoch)
                 + "  AND   epochtimestamp>" + str(minepoch)
                 + "  AND   sensor='" + sensor_name
                 + "' ORDER BY epochtimestamp ASC;")

    date_and_value = curs.fetchall()
    epochdates = list()
    values = list()
    for i in list(range(len(date_and_value))):
        epoch = date_and_value[i][0]
        epoch_minutes = round(epoch / 60.)
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
        graph_title=sensor_name,
        # right_align=False,  # no effect?!
        right_font=False,
        scale_divisions=2,
        show_graph_title=False,
        show_y_labels=not tiny_graph,
        show_x_labels=not tiny_graph,  # Hours below
        # show_x_title=not(tiny_graph),  # Default False, "X Field names" below
        # show_y_title=not(tiny_graph),  # Default False, "Y Scale" on left
        show_graph_subtitle=False,
        show_x_guidelines=False,  # vertical dot lines: One per *value*
        show_y_guidelines=not tiny_graph,  # horizontal dot lines
        stagger_y_labels=False,  # Default False (shift values for readability if too many)
        step_include_first_y_label=False,
        show_legend=False,
        top_font=False,
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
    yield sample_line()


def save_samples():
    # root = os.path.dirname(__file__)
    for sample_name, sample in generate_samples():
        # sample = gen_sample()

        res = sample.burn()
        print(res)


if __name__ == '__main__':
    log.info("Start creating SVG")
    print("Content-type: image/svg+xml; charset=utf-8\r\n\r\n")
    print("""<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\r\n""")
    save_samples()
    log.info("Terminated creating SVG")

