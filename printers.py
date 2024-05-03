
import sys
sys.path.append('src/Python-Thermal-Printer')

from Adafruit_Thermal import *
import numpy as np
from PIL import Image

class DummyPrinter():
    def __init__(self, *args, **kwargs):
        pass

    def println(self, msg,
                n=3,
                **kwargs,
                ):
        print(msg, '\n' * (n + 1), end='')

    def feed(self, **kwargs):
        pass

    def has_paper(self):
        return True


class Printer():
    def __init__(self,
                 stdout: str = '/dev/ttyAMA0',
                 baudrate: int = 19200,
                 timeout: int = 10,
                 mode: str = 'normal',
                 ) -> None:
        """
        must deactivate bluetooth!
        """
        self.printer = Adafruit_Thermal(stdout, baudrate, timeout=timeout)
        self.printer.setSize('s')

        if mode == 'low':
            heat_time = 80
            dot_print_time = 30000
            dot_feed_time = 2100
        elif mode == 'normal':
            heat_time = 120
            dot_print_time = 30000
            dot_feed_time = 2100
        elif mode == 'image':
            heat_time = 120
            dot_print_time = 30000
            dot_feed_time = 2100

        self.printer.begin(heatTime=heat_time)
        #self.printer.setTimes(dot_print_time, dot_feed_time)

    def println(self, msg,
                n=3,
                mode='L',
                ):
        if self.has_paper():
            print(msg)
            self.printer.justify(mode)
            self.printer.println(msg)
            self.printer.justify('L')
            if n > 0:
                self.feed(n)
        else:
            print('no paper')

    def feed(self, n):
        self.printer.feed(n)

    def has_paper(self):
        return self.printer.hasPaper()

    def print_image(self, image_file: Image,
                    LaaT: bool = True,
                    ):
        image = image_file.convert('1')

        width = image.size[0]
        height = image.size[1]
        if width > 384:
            width = 384
        rowBytes = math.floor((width + 7) / 8)
        bitmap = bytearray(rowBytes * height)
        pixels = image.load()

        for y in range(height):
            n = y * rowBytes
            x = 0
            for b in range(rowBytes):
                sum = 0
                bit = 128
                while bit > 0:
                    if x >= width: break
                    if pixels[x, y] == 0:
                        sum |= bit
                    x += 1
                    bit >>= 1
                bitmap[n + b] = sum

        self.printer.printBitmap(width, height, bitmap, LaaT=LaaT)
        
    def print_line(self,
                   height: int = 2,
                   ):
        width = 384
        image = np.full((height, width), fill_value=0, dtype=np.uint8)
        image = Image.fromarray(image)
        self.print_image(image)

