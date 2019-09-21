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


def generate_samples():
    yield 'Line', sample_Line()


def sample_Line():
    form = cgi.FieldStorage()
    sensor = form.getvalue("sensor")
    maxepoch = form.getvalue("maxepoch")
    if maxepoch is None:
        maxepoch = 20000
    
    g = line.Line()
    options = dict(
        scale_integers=True,
        area_fill=True,
        width=640,  # calculations done with width and height, must be integer in pixel ('em' not accepted...)
        height=480,
        fields=['18:00', '', '0:00', '', '6:00', '', '12:00', '', '18:00'],
        graph_title='Question 7',
        show_graph_title=False,
        no_css=False,
    )
    g.__dict__.update(options)
    # g.add_data({'data': [-2, 3, 1, 3, 1], 'title': 'Female'})  # , 'title': 'Female'
    # g.add_data({'data': [11, 10, 9, 9, 9, 9, 10, 11, 14], 'title': 'Temperature'})  # , 'title': 'Female'
    g.add_data({'data': [11.6, 10.4, 9.6, 9.0, 9.3, 9.7, 10.3, 11.7, 14.0], 'title': ''})
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
