#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calendar
import datetime
import time


def epoch_now():
    return calendar.timegm(time.gmtime())


def iso_timestamp_now():
    return datetime.datetime.utcfromtimestamp(epoch_now()).isoformat()


def iso_timestamp(epoch):
    return datetime.datetime.utcfromtimestamp(epoch).isoformat()


def iso_timestamp4files():
    return iso_timestamp_now().replace(':', '-')
