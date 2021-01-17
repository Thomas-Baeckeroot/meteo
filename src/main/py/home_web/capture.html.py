#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi


METEO_FOLDER = "/home/pi/meteo/"
CAPTURES_FOLDER = METEO_FOLDER + "captures/"

print("Content-type: text/html; charset=utf-8\n")
form = cgi.FieldStorage()
image = form.getvalue("image")
#image="grangette/2021/01-10/grangette_2021-01-10Z16-00-07.jpg"
html = """<!DOCTYPE html>
<head>
    <title>Centrale météo St Benoît</title>
    <link rel="icon" type="image/svg+xml" href="html/favicon.svg">
    <style>
        table, th {
          border-collapse: collapse; border: none;
        }
        td {
          text-align: center;
        }
        A {text-decoration: none;}
    </style>
</head>
<body style="background-color: lightsteelblue;">
<h3>Dernières valeurs:</h3>
<table style="width: 100%; height:4.3em;"> <!-- border: .02em solid black -->
<tr style="text-align: left;">
    <td></td> <!-- style="border: none; background-color: transparent;" -->
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">0h / 12h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">1h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">2h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">3h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">4h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">5h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">6h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">7h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">8h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">9h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">10h</td>
    <th colspan="4" style="border: .02em solid black; background-color: whitesmoke;">11h</td>
</tr><tr style="font-size: small;">
    <td style="font-size: medium; border: .02em solid black; background-color: whitesmoke;">am</td>
    
    <td><a href="http://example.com"><div style="height:100%;width:100%">00</div></a></td>
    <td><a href="http://example.com"><div style="height:100%;width:100%">15</div></a></td>
    <td><a href="http://example.com"><div style="height:100%;width:100%">30</div></a></td>
    <td><a href="http://example.com"><div style="height:100%;width:100%">45</div></a></td>
    
    <td><a href="Foo.com">00</a>
    <td><a href="Foo.com">15</a>
    <td><a href="Foo.com">30</a>
    <td><a href="Foo.com">45</a>
    
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
</tr><tr style="font-size: small;"> <!-- text-align: right; -->
    <td style="font-size: medium; border: .02em solid black; background-color: whitesmoke;">pm</td>
    
    <td><a href="http://example.com"><div style="height:100%;width:100%">00</div></a></td>
    <td><a href="http://example.com"><div style="height:100%;width:100%">15</div></a></td>
    <td><a href="http://example.com"><div style="height:100%;width:100%">30</div></a></td>
    <td><a href="http://example.com"><div style="height:100%;width:100%">45</div></a></td>
    
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
    <td>00</td><td>15</td><td>30</td><td>45</td>
</tr>
</table>
<img src=\"captures/""" + image + """\" />
</body></html>"""
print(html)
