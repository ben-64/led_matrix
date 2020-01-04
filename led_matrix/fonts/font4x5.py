#!/usr/bin/env python3

# Taken from https://github.com/pewpew-game/pew-ugame-10.x/blob/master/pew.py

from led_matrix.font import GLCDFont

class Font4x5(GLCDFont):
    HEIGHT = 5
    WIDTH = 4
    FONT = (
        b'{{{{{{wws{w{HY{{{{YDYDY{sUtGU{H[wyH{uHgHE{ws{{{{vyxyv{g[K[g{{]f]{{{wDw{{'
        b'{{{wy{{{D{{{{{{{w{K_w}x{VHHHe{wuwww{`KfyD{UKgKU{w}HDK{DxTKT{VxUHU{D[wyx{'
        b'UHfHU{UHEKe{{w{w{{{w{wy{KwxwK{{D{D{{xwKwx{eKg{w{VIHyB{fYH@H{dHdHd{FyxyF{'
        b'`XHX`{DxtxD{Dxtxx{FyxIF{HHDHH{wwwww{KKKHU{HXpXH{xxxxD{Y@DLH{IL@LX{fYHYf{'
        b'`HH`x{fYHIF{`HH`H{UxUKU{Dwwww{HHHIR{HHH]w{HHLD@{HYsYH{HYbww{D[wyD{txxxt{'
        b'x}w_K{GKKKG{wLY{{{{{{{{Dxs{{{{{BIIB{x`XX`{{ByyB{KBIIB{{WIpF{OwUwww{`YB[`'
        b'x`XHH{w{vwC{K{OKHUxHpXH{vwws_{{dD@H{{`XHH{{fYYf{{`XX`x{bYIBK{Ipxx{{B}_d{'
        b'wUws_{{HHIV{{HH]s{{HLD@{{HbbH{{HHV[a{D_}D{Cw|wC{wwwwwwpwOwp{uxfKW{@YYY@{'
    )

    def draw_char(self, char, x, y, framebuffer, color):
        colors = (color, color, None, None)
        index = min(95, ord(char) - 0x20)

        row = y
        index *= 6
        for byte in self.FONT[index:index + 6]:
            # Python3 or Python2
            if type(byte) is int:
                unsalted = byte ^ 132
            else:
                unsalted = ord(byte) ^ 132
            for col in range(x, x + 4):
                color = colors[unsalted & 0x03]
                if color is not None:
                    framebuffer.pixel(col,row,color)
                unsalted >>= 2
            row += 1
