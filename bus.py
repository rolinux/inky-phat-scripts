#!/usr/bin/python3

import urllib.request
import json
from datetime import datetime
import time
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

def my_draw(message):
  inky_display = InkyPHAT("black")
  inky_display.set_border(inky_display.WHITE)

  img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
  draw = ImageDraw.Draw(img)

  font = ImageFont.truetype(FredokaOne, 30)

  w, h = font.getsize(message)
  #x = (inky_display.WIDTH / 2) - (w / 2)
  #y = (inky_display.HEIGHT / 2) - (h / 2)
  x = 1
  y = 1
      
  draw.text((x, y), message, inky_display.BLACK, font)
  inky_display.set_image(img)
  inky_display.show()

while True:
  with urllib.request.urlopen('http://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1?StopID=20515&LineName=89&ReturnList=LineName,ExpireTime') as response:
    text = response.read().decode('utf-8')

  now = datetime.now()

  buses = []
  for line in text.split("\r\n"):
    j = json.loads(line)
    if j[1] == "89":
      bus_time = datetime.fromtimestamp(j[2]/1000.0)
      diff_time = int(round((bus_time - now).total_seconds() / 60.0))
      if diff_time > 4:
        buses.append('%s (%s)' % (diff_time, datetime.fromtimestamp(j[2]/1000.0).strftime("%H:%M")))
      else:
       print('%s bus is too close to catch up' % datetime.fromtimestamp(j[2]/1000.0).strftime("%H:%M"))
  
  message = '\n'.join(buses)
  print(message)

  my_draw(message)

  time.sleep(60)
