#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os

# import psycopg2 as db_module  # ProgreSQL library
# import mariadb as db_module  # MariaDB library
# import mysql.connector as db_module  # MySQL library
import pymysql as db_module  # PyMySQL


def get_conn(host=None):
    home = os.path.expanduser("~")  # if failing here, test "from pathlib import Path / home = str(Path.home())"
    config = configparser.ConfigParser()
    config.read(home + '/.config/meteo.conf')
    database = config.get('DATABASE', 'Name', fallback='weather_station')
    user = config.get('DATABASE', 'User')  # Could have default fallback to os.getusername()
    password = config['DATABASE']['Password']
    port = config.getint('DATABASE', 'Port', fallback=3306)

    if host is None:
        conn = db_module.connect(
            database=database,
            user=user,
            password=password,
            port=port)
    else:
        conn = db_module.connect(
            server=host,
            database=database,
            user=user,
            password=password,
            port=port)

    return conn
