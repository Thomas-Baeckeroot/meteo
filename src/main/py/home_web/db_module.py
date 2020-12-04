#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os

# import psycopg2 as db_module  # PostgreSQL library
# import mariadb as db_module  # MariaDB library
# import mysql.connector as db_module  # MySQL library
import pymysql as db_module  # PyMySQL


def get_conn(host=None):
    home = os.path.expanduser("~")  # if failing here, test "from pathlib import Path / home = str(Path.home())"
    config = configparser.ConfigParser()
    config.read(home + '/.config/meteo.conf')  # todo rename to weather_station.conf

    if host is None:
        database = config.get('DATABASE', 'Name', fallback='weather_station')
        user = config.get('DATABASE', 'User')  # Could have default fallback to os.getusername()
        password = config.get('DATABASE', 'Password')
        port = config.getint('DATABASE', 'Port', fallback=3306)
        conn = db_module.connect(
            database=database,
            user=user,
            password=password,
            port=port)
    else:
        database = config.get('remote:' + host, 'Name', fallback='weather_station')
        user = config.get('remote:' + host, 'User')  # Could have default fallback to os.getusername()
        password = config.get('remote:' + host, 'Password')
        port = config.getint('remote:' + host, 'Port', fallback=3306)
        conn = db_module.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port)

    return conn
