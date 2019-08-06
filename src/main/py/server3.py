#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Sample based from https://python-django.dev/page-python-serveur-web-creer-rapidement

import http.server
import cgitb

cgitb.enable()

PORT = 49107
server_address = ("", PORT)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["/"]
print("Serveur P3 actif sur le port: " + str(PORT))

httpd = server(server_address, handler)
httpd.serve_forever()
