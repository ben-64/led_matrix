#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json

from led_matrix.images.image import Image
from led_matrix.fonts.adafruit import *
from led_matrix.animation.animation import TextApplication

SUN = [0x0, 0x0, 0xffe900, 0x0, 0x0, 0xffe900, 0x0, 0x0, 0xffe900, 0x0, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0x0, 0xffe900, 0x0, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0x0, 0x0, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0x0, 0x0, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0x0, 0x0, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0x0, 0xffe900, 0x0, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0x0, 0xffe900, 0x0, 0x0, 0xffe900, 0x0, 0x0, 0xffe900, 0x0, 0x0 ];
CLOUDY = [0x0, 0x0, 0x0, 0xFFFFFF, 0xFFFFFF, 0x0, 0x0, 0x0, 0x0, 0x0, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0x0, 0x0, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0x0, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0x0, 0x0, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0 ];
RAIN = [0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x0, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x0, 0x4b39, 0x0, 0x333333, 0x333333, 0x333333, 0x333333, 0x0, 0x4b39, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4b39, 0x0, 0x0, 0x0, 0x4b39, 0x0, 0x4b39, 0x0, 0x0, 0x4b39, 0x0, 0x4b39, 0x0, 0x0, 0x0, 0x0, 0x4b39, 0x0, 0x4b39, 0x0, 0x0, 0x4b39, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4b39, 0x0, 0x0, 0x4b39, 0x0, 0x0, 0x4b39, 0x0 ];
PARTLYCLOUDY = [0x0, 0x0, 0xffe900, 0x0, 0x0, 0xffe900, 0x0, 0x0, 0xffe900, 0x0, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0x0, 0xffe900, 0x0, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0x0, 0x0, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0xffe900, 0x0, 0xffe900, 0xffff, 0xffff, 0xffe900, 0xffe900, 0xffff, 0xffff, 0xffe900, 0xffff, 0xffff, 0xffff, 0xffff, 0xffe900, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0x0, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0x0 ];
BAD_CLOUD = [0x0, 0x0, 0x0, 0x333333, 0x333333, 0x0, 0x0, 0x0, 0x0, 0x0, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x0, 0x0, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x0, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x0, 0x0, 0x333333, 0x333333, 0x333333, 0x333333, 0x333333, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0 ];
THUNDER = [0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0x0, 0x0, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xffec, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xffec, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xffec, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xffec, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xffec, 0x0, 0x0, 0x0, 0x0 ];
SNOW = [0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0x0, 0x0, 0xb596, 0xb596, 0xb596, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xffff, 0x0, 0x0, 0xffff, 0x0, 0x0, 0xffff, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xffff, 0x0, 0x0, 0x0, 0xffff, 0x0, 0xffff, 0x0, 0x0, 0x0, 0xffff, 0x0, 0x0, 0x0 ];
MIST = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0 ];


class OpenWeatherData(TextApplication):
    METEO_ICON = {"01":SUN,"02":PARTLYCLOUDY,"03":CLOUDY,"04":BAD_CLOUD,"09":RAIN,"10":RAIN,"11":THUNDER,"13":SNOW,"50":MIST}

    def __init__(self,api_key,city,*args,**kargs):
        super().__init__(*args,**kargs)
        self.api_key = api_key
        self.city = city
        self.font = AdaFruit(2)

    def update(self):
        x = urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?APPID=%s&id=%s&units=metric" % (self.api_key,self.city))
        j = json.loads(x.read().decode("utf-8"))
        weather,temp =  j["weather"][0]["icon"][:-1],j["main"]["temp"]
        self.set_icon(Image(self.METEO_ICON.get(weather,SUN),8,8))
        self.print_text("%u°" % int(float(temp)))


