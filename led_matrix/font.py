#!/usr/bin/env python3

class Font(object):
    def draw_char(self, char, x, y, framebuffer, color):
        raise NotImplementedError()

class GLCDFont(Font):
    FONT = None
    HEIGHT = None
    WIDTH = None

    def draw_char(self, char, x, y, framebuffer, color):
        """Draw one character at position (x,y) to a framebuffer in a given color"""
        # Don't draw the character if it will be clipped off the visible area.
        if x < -self.WIDTH or x >= framebuffer.width or \
           y < -self.HEIGHT or y >= framebuffer.height:
            return
        # Go through each column of the character.
        for char_x in range(self.WIDTH):
            # Grab the byte for the current column of font data.
            line = self[char][char_x] if type(self[char][char_x]) is int else int(self[char][char_x])
            # Go through each row in the column byte.
            for char_y in range(self.HEIGHT):
                # Draw a pixel for each bit that's flipped on.
                if (line >> char_y) & 0x1:
                    framebuffer.pixel(x + char_x, y + char_y, color)

    def width(self, text):
        """Return the pixel width of the specified text message."""
        return len(text) * (self.WIDTH)

    def __getitem__(self,i):
        return self.FONT[ord(i)*self.WIDTH:ord(i)*(self.WIDTH+1)]
