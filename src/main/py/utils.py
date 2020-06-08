#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import time


def epoch_now():
    # return calendar.timegm(time.gmtime())
    return int(time.time())


def iso_timestamp_now():  # example: 2020-05-03T15:49:48
    return iso_timestamp(epoch_now())


def iso_timestamp(epoch):
    return datetime.datetime.utcfromtimestamp(epoch).isoformat(sep='Z')


def iso_timestamp4files():
    return iso_timestamp_now().replace(':', '-')


def local_timestamp_now():  # example: 2020-05-03T15:49:48
    return local_timestamp(epoch_now())


def local_timestamp(epoch):
    if time.localtime().tm_isdst and time.daylight:
        separator = 'S'  # Summer time
    else:
        separator = 'W'  # Winter time
    return datetime.datetime.fromtimestamp(epoch).isoformat(sep=separator)
