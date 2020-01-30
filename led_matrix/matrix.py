#!/usr/bin/env python

import sys
import time

try:
    import _rpi_ws281x as ws
except:
    print("No driver for ws281x")

from led_matrix.screen import Screen

class LEDMatrix(Screen):
    DEFAULT_COLOR = 0

    def __init__(self,height=8,width=32,brightness=50,gpio=18):
        Screen.__init__(self,width,height)
        self.brightness = brightness
        self.led_channel = 0
        self.freq_hz = 800000
        self.dma_num = 10
        self.gpio = gpio
        self.invert = 0
        try:
            self.leds = ws.new_ws2811_t()
        except NameError:
            print("Driver missing")
            sys.exit(1)
        self.init()

    def init(self):
        self.channel_off()
        self.channel = ws.ws2811_channel_get(self.leds, self.led_channel)
        ws.ws2811_channel_t_count_set(self.channel, self.height*self.width)
        ws.ws2811_channel_t_gpionum_set(self.channel, self.gpio)
        ws.ws2811_channel_t_invert_set(self.channel, self.invert)
        ws.ws2811_channel_t_brightness_set(self.channel, self.brightness)

        ws.ws2811_t_freq_set(self.leds, self.freq_hz)
        ws.ws2811_t_dmanum_set(self.leds, self.dma_num)

        # Initialize library with LED configuration.
        resp = ws.ws2811_init(self.leds)
        if resp != ws.WS2811_SUCCESS:
            message = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, message))
        print("init success")

    def colorwipe(self):
        """Wipe color across display a pixel at a time."""
        self.fill(0)

    def stop(self):
        self.colorwipe()
        self.render()
        ws.ws2811_fini(self.leds)
        ws.delete_ws2811_t(self.leds)

    def channel_off(self):
        # Initialize all channels to off
        for channum in range(2):
            channel = ws.ws2811_channel_get(self.leds, channum)
            ws.ws2811_channel_t_count_set(channel, 0)
            ws.ws2811_channel_t_gpionum_set(channel, 0)
            ws.ws2811_channel_t_invert_set(channel, 0)
            ws.ws2811_channel_t_brightness_set(channel, 0)

    def set_pixel(self,x,y,color):
        color = ((color&0xFF00)<<8) | ((color&0xFF0000)>>8) | color&0xFF
        ws.ws2811_led_set(self.channel, self.compute_index(x,y), color)

    def compute_index(self,i,j):
        if i%2 == 0:
            return i*self.height+j
        else:
            return i*self.height+(self.height-j-1)

    def from_iso_index(self,index):
        x = index%self.width
        y = int(index/self.width)
        return self.compute_index(x,y)

    def render(self):
        resp = ws.ws2811_render(self.leds)
        if resp != ws.WS2811_SUCCESS:
            message = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))
