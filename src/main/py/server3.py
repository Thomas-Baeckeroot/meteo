#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample based from https://python-django.dev/page-python-serveur-web-creer-rapidement

import http.server
import cgitb
# import logging
import sys

from utils import get_config

# Due to Logger unable to get error message details, then it has been commented.
# Outputs will tentatively be catch by redirection on call.


class LoggerWriter:
    def __init__(self, level):
        # self.level is really like using log.debug(message)
        # at least in my case
        self.level = level
                                    
    def write(self, message):
        # if statement reduces the amount of newlines that are
        # printed to the logger
        if message != '\n':
            self.level(message)
                                                                                    
    def flush(self):
        # create a flush method so things can be flushed when
        # the system wants to. Not sure if simply 'printing'
        # sys.stderr is the correct way to do it, but it seemed
        # to work properly for me.
        self.level(sys.stderr)
        

# print = logging.info

# logging.basicConfig(filename='/home/web/server3.log',level=logging.DEBUG)

# log = logging.getLogger()
# sys.stdout = LoggerWriter(log.info)
# sys.stderr = LoggerWriter(log.warning)

# logging.info('log started - INFO level')
# logging.error('log started - ERROR level')

cgitb.enable()

config = get_config()
port = config.getint('DEFAULT', 'WebServerPort', fallback=8080)
server_address = ("", port)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["/"]
print("Serveur P3 actif sur le port: " + str(port))

httpd = server(server_address, handler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nKeyboard interruption intercepted. Exiting...")
