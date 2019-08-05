#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Sample based from https://python-django.dev/page-python-serveur-web-creer-rapidement

import BaseHTTPServer
import CGIHTTPServer

PORT = 49107
server_address = ("", PORT)

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
handler.cgi_directories = ["/"]
print "Serveur actif sur le port :", PORT

httpd = server(server_address, handler)
httpd.serve_forever()
