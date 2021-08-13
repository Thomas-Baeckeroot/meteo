#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import PIL


fp_in = "/home/thomas/workspace/meteo/captures/grangette/2021/03-09_/grangette_2021-03-09Z*.jpg"
fp_out = "/home/thomas/workspace/meteo/captures/grangette/2021/03-09_daytime_down.gif"

img, *imgs = [PIL.Image.open(f) for f in sorted(glob.glob(fp_in))]

new_size = (648, 486)
img = img.resize(new_size)

images = []
for i in imgs:
    images.append(i.resize(new_size))

img.save(
    fp=fp_out,
    format='GIF',
    append_images=images,
    save_all=True,
    duration=200,
    loop=0)

# img2.save(fp="/home/thomas/workspace/meteo/captures/grangette/2021/03-09_daytime_2.gif", format='GIF', append_images=imgs, save_all=True, duration=200, loop=0)
