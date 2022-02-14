import board
import neopixel
from threading import Thread
import time

class LEDArray:

    """
    Class for controlling the LED array
    """

    def __init__(self) -> None:
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        self.pixel_pin = board.D18
        
        # The number of NeoPixels
        self.num_pixels = 24
        
        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        self.ORDER = neopixel.GRB
        
        # Setup main pixels object
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
        )

    def listening(self):
        pass
        # Run the listening animation

    def speaking(self):
        pass
        # Run the speaking animation

    def loading(self):
        pass
        # Run the processing animation

    def reset(self):
        pass
        # Turn off all LEDs
        
    def wheel(self, pos):
         # Input a value 0 to 255 to get a color value.
         # The colours are a transition r - g - b - back to r.
         if pos < 0 or pos > 255:
            r = g = b = 0
         elif pos < 85:
             r = int(pos * 3)
             g = int(255 - pos * 3)
             b = 0
         elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
         else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
         return (r, g, b) if self.ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
    
    def rainbow_cycle(self, wait):
         for j in range(255):
             for i in range(self.num_pixels):
                 pixel_index = (i * 256 // self.num_pixels) + j
                 self.pixels[i] = self.wheel(pixel_index & 255)
                 self.pixels.show()
                 time.sleep(wait)
