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
    yield 'VerticalBar', SampleBar.vertical()
    yield 'HorizontalBar', SampleBar.horizontal()
    yield 'VerticalBarLarge', SampleBar.vertical_large()
    yield 'VerticalBarStackTop', SampleBar.vertical_top()
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
    g.add_data({'data': [-2, 3, 1, 3, 1]})  # , 'title': 'Female'
    # g.add_data({'data': [0, 2, 1, 5, 4], 'title': 'Male'})
    return g


def save_samples():
    root = os.path.dirname(__file__)
    for sample_name, sample in generate_samples():
        res = sample.burn()
        with open(os.path.join(root, sample_name + '.py.svg'), 'w') as f:
            f.write(res)


if __name__ == '__main__':
    save_samples()
