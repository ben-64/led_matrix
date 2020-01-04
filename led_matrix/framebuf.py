#!/usr/bin/env python3

import struct

from led_matrix.fonts.adafruit import AdaFruit

class MHMSBFormat:
    """MHMSBFormat"""
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        index = (y * framebuf.stride + x) // 8
        offset = 7 - x & 0x07
        framebuf.buf[index] = (framebuf.buf[index] & ~(0x01 << offset)) | ((color != 0) << offset)

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel"""
        index = (y * framebuf.stride + x) // 8
        offset = 7 - x & 0x07
        return (framebuf.buf[index] >> offset) & 0x01

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        # pylint: disable=too-many-arguments
        for _x in range(x, x+width):
            offset = 7 - _x & 0x07
            for _y in range(y, y+height):
                index = (_y * framebuf.stride + _x) // 8
                framebuf.buf[index] = (framebuf.buf[index] & ~(0x01 << offset)) \
                                      | ((color != 0) << offset)

class MVLSBFormat:
    """MVLSBFormat"""
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        index = (y >> 3) * framebuf.stride + x
        offset = y & 0x07
        framebuf.buf[index] = (framebuf.buf[index] & ~(0x01 << offset)) | ((color != 0) << offset)

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel"""
        index = (y >> 3) * framebuf.stride + x
        offset = y & 0x07
        return (framebuf.buf[index] >> offset) & 0x01

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        # pylint: disable=too-many-arguments
        while height > 0:
            index = (y >> 3) * framebuf.stride + x
            offset = y & 0x07
            for w_w in range(width):
                framebuf.buf[index + w_w] = (framebuf.buf[index + w_w] & ~(0x01 << offset)) |\
                                           ((color != 0) << offset)
            y += 1
            height -= 1


class RGB565Format:
    """RGB565Format"""
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        index = (x + y * framebuf.stride) * 2
        framebuf.buf[index] = (color >> 8) & 0xFF
        framebuf.buf[index + 1] = color & 0xFF

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel"""
        index = (x + y * framebuf.stride) * 2
        return (framebuf.buf[index] << 8) | framebuf.buf[index + 1]

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        # pylint: disable=too-many-arguments
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        while height > 0:
            for w_w in range(width):
                index = (w_w + x + y * framebuf.stride) * 2
                framebuf.buf[index] = (color >> 8) & 0xFF
                framebuf.buf[index + 1] = color & 0xFF
            y += 1
            height -= 1


class OneByteFormat:
    """RGB565Format"""
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        index = (x + y * framebuf.stride)
        framebuf.buf[index] = color

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel"""
        index = (x + y * framebuf.stride)
        return framebuf.buf[index]

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        # pylint: disable=too-many-arguments
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        while height > 0:
            for w_w in range(width):
                index = (w_w + x + y * framebuf.stride)
                framebuf.buf[index] = color
            y += 1
            height -= 1

class FrameBuffer:
    """FrameBuffer object.

    :param buf: An object with a buffer protocol which must be large enough to contain every
                pixel defined by the width, height and format of the FrameBuffer.
    :param width: The width of the FrameBuffer in pixel
    :param height: The height of the FrameBuffer in pixel
    :param buf_format: Specifies the type of pixel used in the FrameBuffer; permissible values
                        are listed under Constants below. These set the number of bits used to
                        encode a color value and the layout of these bits in ``buf``. Where a
                        color value c is passed to a method, c is  a small integer with an encoding
                        that is dependent on the format of the FrameBuffer.
    :param stride: The number of pixels between each horizontal line of pixels in the
                   FrameBuffer. This defaults to ``width`` but may need adjustments when
                   implementing a FrameBuffer within another larger FrameBuffer or screen. The
                   ``buf`` size must accommodate an increased step size.

    """
    def __init__(self, buf, width, height, buf_format=OneByteFormat, stride=None):
        # pylint: disable=too-many-arguments
        self.buf = buf
        self.width = width
        self.height = height
        self.stride = stride
        self._font = None
        if self.stride is None:
            self.stride = width
        self.format = buf_format()

    def fill(self, color):
        """Fill the entire FrameBuffer with the specified color."""
        self.format.fill_rect(self, 0, 0, self.width, self.height, color)

    def fill_rect(self, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        # pylint: disable=too-many-arguments, too-many-boolean-expressions
        if width < 1 or height < 1 or (x + width) <= 0 or (y + height) <= 0 or y >= self.height \
                or x >= self.width:
            return
        x_end = min(self.width, x + width)
        y_end = min(self.height, y + height)
        x = max(x, 0)
        y = max(y, 0)
        self.format.fill_rect(self, x, y, x_end - x, y_end - y, color)

    def pixel(self, x, y, color=None):
        """If ``color`` is not given, get the color value of the specified pixel. If ``color`` is
        given, set the specified pixel to the given color."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        if color is None:
            return self.format.get_pixel(self, x, y)
        self.format.set_pixel(self, x, y, color)
        return None

    def hline(self, x, y, width, color):
        """Draw a horizontal line up to a given length."""
        self.fill_rect(x, y, width, 1, color)

    def vline(self, x, y, height, color):
        """Draw a vertical line up to a given length."""
        self.fill_rect(x, y, 1, height, color)

    def rect(self, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ```rect``` method draws only
        a 1 pixel outline."""
        # pylint: disable=too-many-arguments
        self.fill_rect(x, y, width, 1, color)
        self.fill_rect(x, y + height-1, width, 1, color)
        self.fill_rect(x, y, 1, height, color)
        self.fill_rect(x + width - 1, y, 1, height, color)

    def line(self, x_0, y_0, x_1, y_1, color):
        # pylint: disable=too-many-arguments
        """Bresenham's line algorithm"""
        d_x = abs(x_1 - x_0)
        d_y = abs(y_1 - y_0)
        x, y = x_0, y_0
        s_x = -1 if x_0 > x_1 else 1
        s_y = -1 if y_0 > y_1 else 1
        if d_x > d_y:
            err = d_x / 2.0
            while x != x_1:
                self.pixel(x, y, color)
                err -= d_y
                if err < 0:
                    y += s_y
                    err += d_x
                x += s_x
        else:
            err = d_y / 2.0
            while y != y_1:
                self.pixel(x, y, color)
                err -= d_x
                if err < 0:
                    x += s_x
                    err += d_y
                y += s_y
        self.pixel(x, y, color)

    def blit(self):
        """blit is not yet implemented"""
        raise NotImplementedError()

    def scroll(self, delta_x, delta_y):
        """shifts framebuf in x and y direction"""
        if delta_x < 0:
            shift_x = 0
            xend = self.width + delta_x
            dt_x = 1
        else:
            shift_x = self.width - 1
            xend = delta_x - 1
            dt_x = -1
        if delta_y < 0:
            y = 0
            yend = self.height + delta_y
            dt_y = 1
        else:
            y = self.height - 1
            yend = delta_y - 1
            dt_y = -1
        while y != yend:
            x = shift_x
            while x != xend:
                self.format.set_pixel(
                    self, x, y, self.format.get_pixel(self, x - delta_x, y - delta_y))
                x += dt_x
            y += dt_y

    def text(self, string, x, y, color, font=AdaFruit()):
        w = font.WIDTH
        for i, char in enumerate(string):
            font.draw_char(char=char,x=x + (i * (w+1)),y=y,framebuffer=self,color=color)

    def image(self, img):
        """Set buffer to value of Python Imaging Library image.  The image should
        be in 1 bit mode and a size equal to the display size."""
        if img.mode != '1':
            raise ValueError('Image must be in mode 1.')
        imwidth, imheight = img.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display ({0}x{1}).' \
                .format(self.width, self.height))
        # Grab all the pixels from the image, faster than getpixel.
        pixels = img.load()
        # Clear buffer
        for i in range(len(self.buf)):
            self.buf[i] = 0
        # Iterate through the pixels
        for x in range(self.width):       # yes this double loop is slow,
            for y in range(self.height):  #  but these displays are small!
                if pixels[(x, y)]:
                    self.pixel(x, y, 1)   # only write if pixel is true
