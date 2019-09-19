#!/usr/bin/python3
# coding: utf-8

"""
Samples of the various charts. Run this script to generate the reference
samples.
"""

import os

from svg.charts.plot import Plot
from svg.charts import bar
from svg.charts import time_series
from svg.charts import pie
from svg.charts import schedule
from svg.charts import line


def generate_samples():
    yield 'Line', sample_Line()


def sample_Line():
    g = line.Line()
    options = dict(
        scale_integers=True,
        area_fill=True,
        width=640,
        height=480,
        fields=['Internet', 'TV', 'Newspaper', 'Magazine', 'Radio'],
        graph_title='Question 7',
        show_graph_title=True,
        no_css=False,
    )
    g.__dict__.update(options)
    g.add_data({'data': [-2, 3, 1, 3, 1], 'title': 'Female'})  # , 'title': 'Female'
    # g.add_data({'data': [0, 2, 1, 5, 4], 'title': 'Male'})
    return g


def gen_sample():
    yield sample_Line()


def save_samples():
    root = os.path.dirname(__file__)
    for sample_name, sample in generate_samples():
    #sample = gen_sample()

        res = sample.burn()
        print(res)


if __name__ == '__main__':
    save_samples()
