#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample based from https://python-django.dev/page-python-serveur-web-creer-rapidement

import http.server
import cgitb
import logging
import os
import signal
import sys

from utils import get_config
from public_html.db_module import get_home


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


def file_exists(filename):
    if os.path.exists(filename):
        # log.debug(f"File '{filename}' exists in the current folder.")
        return True
    else:
        log.debug(f"File '{filename}' not found in the current folder.")
        return False


def check_symlinks():
    for filename in ["capture.html", "captures.json", "graph.svg", "index.html"]:  # finishing with "index.html"
        if file_exists(filename):
            log.debug(f"File '{filename}' found in working directory.")
        else:
            if file_exists(filename + ".py"):
                os.symlink(filename + ".py", filename)
                log.warning(f"Symbolic link '{filename}' -> '{filename}.py' created in working directory.")
            else:
                log.error(f"Failed to find '{filename}.py' in working directory!")
    return


def current_dir_is_valid_working_dir():
    if file_exists("index.html") or file_exists("index.html.py"):
        log.debug(f"Current folder looks good as working directory for server.")
        return True
    else:
        log.info("Working directory does not contain expected files for web server.")
        log.warning("Please review the way the server is launched: "
                    "it should be launched from the folder that contains 'index.html', etc...")
        return False


def check_working_dir():
    # Path of Python 3 binary (Virtual Env.):
    log.info("Path to Python binary (expected starting with venv): {0}".format(sys.executable))

    # Working path: server should be started from the folder containing index.html(.py)
    if not current_dir_is_valid_working_dir():
        if file_exists("public_html"):
            os.chdir("public_html")
            if not current_dir_is_valid_working_dir():
                os.chdir(get_home())
                if not current_dir_is_valid_working_dir():
                    log.critical("Unable to find pages to serve!")
        else:
            os.chdir(get_home())
            # TODO Server should start by default in "~/public_html/" ('captures' folder has to be moved there also)
            if not current_dir_is_valid_working_dir():
                log.critical("Unable to find pages to serve!")

    check_symlinks()

    return


def check_python_modules():
    log.info("Checking list of modules available in current environment...")
    required_modules = ["pymysql", "svg.charts"]
    i = 1
    for module_name, module in sys.modules.items():
        # log.debug("  - {:3d} - {}".format(i, module_name))
        if module_name in required_modules:
            required_modules.remove(module_name)
        i += 1

    if required_modules:
        log.error("The following required modules are missing:")
        for missing_module in required_modules:
            log.error("- {}".format(missing_module))
    else:
        log.info("All required modules are present.")


signal.signal(signal.SIGTERM, sigterm_handler)

HOME = get_home()

# Due to Logger unable to get error message details, then it has been commented.
# Outputs will tentatively be caught by redirection on call.

logging.basicConfig(
    filename=HOME + "/susanoo-web.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8.8s%(name)-14s (%(process)5d) %(message)s')
log = logging.getLogger("server3.py")
print(f"HTTP server log is sent to '{HOME}/susanoo-web.log'.")
log.info("Starting ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

check_working_dir()

check_python_modules()

cgitb.enable()

config = get_config()
port = config.getint('DEFAULT', 'WebServerPort', fallback=8080)
server_address = ("", port)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
# handler.cgi_directories = ["~/public_html/"]  # Should be better if other than '/' but never worked...
handler.cgi_directories = ["/"]
log.debug("Launching server from path '{0}' on port {1}...".format(os.getcwd(), port))
log.debug(f"Handler.cgi_directories = {handler.cgi_directories}")

httpd = server(server_address, handler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    log.info("Keyboard interruption intercepted. Exiting gracefully...")
    log.info("Terminating _____________________________________________\n")
    close_server()
