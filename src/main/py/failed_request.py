#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils
import logging

logging.basicConfig(
    filename=utils.get_home() + "/meteo/logfile.log",
    level=logging.DEBUG,
    format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s')
log = logging.getLogger("failed_request.py")

request_file = utils.get_home() + "/meteo/failed_request.sql"


def append(request):
    if len(request) == 0:
        log.error("Dropping an empty line that should not have been there!")
        return
    with open(request_file, "a") as fappend:
        fappend.write(request + "\n")
    log.debug("Appending request to failed_request.sql: " + request)
    return


def extract_first():
    try:
        with open(request_file, 'r') as fin:
            data = fin.read().splitlines(True)
    except FileNotFoundError:
        log.warning("File '" + str(request_file) + "' was not found => no request to extract, returning None.")
        return None
    if len(data) == 0:
        log.debug("No request in file '" + str(request_file) + "', remaining empty and returning None.")
        return None
    with open(request_file, 'w') as fout:
        fout.writelines(data[1:])
    return data[0].rstrip()


def fix_previously_failed_requests(conn):
    previously_failed_requests = extract_first()
    if previously_failed_requests:
        log.debug("Tentatively re-executing request:" + previously_failed_requests)
        try:
            curs = conn.cursor()
            curs.execute(previously_failed_requests)
            curs.close()
            conn.commit()
            log.info("SQL request executed with success.")
        except Exception as e:
            log.debug(e)
            log.warning("SQL request failed (again).")
            append(previously_failed_requests)
    return
