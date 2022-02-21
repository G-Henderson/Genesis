from time import sleep
import board
import neopixel
from threading import Thread
import RPi.GPIO as GPIO

class LEDArray:

    """
    Class for controlling the LED array
    """

    def __init__(self) -> None:
        # Setup neopixel variables
        pixel_pin = board.D12 # GPIO 12
        self.num_pixels = 24 # The number of LEDs
        ORDER = neopixel.RGB # The order of pixel colours
        pixel_brightness = 0.2 # Set the max brightness to 20%
        self.exit_flag = False

        # Setup neopixel ring
        self.pixels = neopixel.NeoPixel(
            pixel_pin, self.num_pixels, brightness=pixel_brightness, auto_write=False, pixel_order=ORDER
        )

        # Set pixels to neutral colour
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

        # OLD LED
        GPIO.setmode(GPIO.BCM) # Setup the old GPIO led
        GPIO.setwarnings(False)
        GPIO.setup(25,GPIO.OUT)

        GPIO.output(25,0) # Make sure it's off

    def listening(self):
        # Run the listening animation
        for i in range(int(self.num_pixels/2)):
            self.pixels[i] = (0, 0, 255)
            self.pixels[(self.num_pixels - i) - 1] = (0, 0, 255)

            self.pixels.show()
            sleep(0.01)

        GPIO.output(25,1) # Turn on the old LED

    def run_speaking(self):
        """
        Method that runs in the background to run
        the speaking animation
        """

        while True:
            if (self.exit_flag): # Check if should stop animating
                break

            for i in range(0, 255, 2):
                self.pixels.fill((0, 0, i))
                self.pixels.show()
                sleep(0.005)

                if (self.exit_flag): # Check if should stop animating
                    break

            if (self.exit_flag): # Check if should stop animating
                break

            for i in range(255, 0, -2):
                self.pixels.fill((0, 0, i))
                self.pixels.show()
                sleep(0.005)

                if (self.exit_flag): # Check if should stop animating
                    break

    def speaking(self):
        """
        Method that starts the thread to play 
        the speaking animation
        """

        self.exit_flag = False
        self.speaking_thread = Thread(target=self.run_speaking)
        self.speaking_thread.start()

    def run_loading(self):
        """
        The method that runs in the background
        to run the processing animation
        """

        ite = 0
        while True:
            if (self.exit_flag):
                break

            q = 24 * ite
            for i in range(self.num_pixels):
                for x in range(self.num_pixels):
                    if (x-q >= i) and (x-q <= i+10):
                        self.pixels[x] = (200, 0, 255)

                    else:
                        self.pixels[x] = (0, 0, 128)

                self.pixels.show()
                sleep(0.07)

            if (ite < 23):
                ite += 1
            else:
                ite = 0

    def loading(self):
        """
        Method that calls the processing animation
        and starts the thread
        """

        self.exit_flag = False
        self.processing_thread = Thread(target=self.run_loading)
        self.processing_thread.start()

    def reset(self):
        # Try stopping the processing animation (if running...)
        if (self.processing_thread != None):
            try:
                self.exit_flag = True
                self.processing_thread.join()
                self.processing_thread = None
            except:
                pass

        # Try stopping the speaking animation (if running...)
        if (self.speaking_thread != None):
            try:
                self.exit_flag = True
                self.speaking_thread.join()
                self.speaking_thread = None
            except:
                pass

        # Turn off all LEDs
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
