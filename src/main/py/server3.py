#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample based from https://python-django.dev/page-python-serveur-web-creer-rapidement

import http.server
import cgitb
import logging
import signal
import sys

from utils import get_config
from home_web.db_module import get_home


def sigterm_handler(signum, frame):
    log.info("Received SIGTERM signal. Exiting gracefully...")
    close_server()


def close_server():
    # Close the server socket to stop accepting new connections
    try:
        httpd.socket.close()
    except Exception as e:
        log.error(f"Error while closing the server socket: {e}")
    sys.exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)

HOME = get_home()

# Due to Logger unable to get error message details, then it has been commented.
# Outputs will tentatively be catch by redirection on call.

logging.basicConfig(
    filename= HOME + "/server3.log",  # = "/home/web/server3.log"
    level=logging.DEBUG,
    format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s')
log = logging.getLogger("server3.py")


log.info("Path to Python binary (expected starting with venv): {0}".format(sys.executable))

log.info("Checking list of modules available in current environment...")
required_modules = ["pymysql", "chart.svg"]
i = 1
for module_name, module in sys.modules.items():
    log.debug("  - {:3d} - {}".format(i, module_name))
    if module_name in required_modules:
        required_modules.remove(module_name)
    i += 1

if required_modules:
    log.error("The following required modules are missing:")
    for missing_module in required_modules:
        log.error("- {}".format(missing_module))
else:
    log.info("All required modules are present.")

cgitb.enable()

config = get_config()
port = config.getint('DEFAULT', 'WebServerPort', fallback=8080)
server_address = ("", port)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
# handler.cgi_directories = ["/home_web/"]  # Should be better if other than '/' but never worked...
handler.cgi_directories = ["/"]
log.debug("Serveur P3 actif sur le port: " + str(port))
log.debug("handler.cgi_directories = ")
log.debug(handler.cgi_directories)

httpd = server(server_address, handler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    log.info("Keyboard interruption intercepted. Exiting gracefully...")
    close_server()
