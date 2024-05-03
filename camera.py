import sys
sys.path.append('src/Python-Thermal-Printer')

import os
import argparse

from Adafruit_Thermal import *

from PIL import Image, ImageEnhance
import numpy as np
import cv2


def print_image(printer, image_file, LaaT=False):
	# image = Image.open(image_file)
	image = image_file
	if image.mode != '1':
		image = image.convert('1')

	width  = image.size[0]
	height = image.size[1]
	if width > 384:
		width = 384
	rowBytes = math.floor((width + 7) / 8)
	bitmap   = bytearray(rowBytes * height)
	pixels   = image.load()

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
				x    += 1
				bit >>= 1
			bitmap[n + b] = sum

	printer.printBitmap(width, height, bitmap, LaaT)

print('a')
printer = Adafruit_Thermal('/dev/ttyAMA0', 19200, timeout=5)  # must deactivate bluetooth!
#printer = Adafruit_Thermal('/dev/serial0', 19200, timeout=5)  # must deactivate bluetooth!
printer.setTimes(30000, 2100)

# Parser and settings.
parser = argparse.ArgumentParser(prefix_chars='--')
parser.add_argument('--factor', default=1.75, type=float)
margs = parser.parse_args()



import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)



printer.println("camera ready")
N = 3
printer.feed(N)
while True: # Run forever
    if GPIO.input(12) == GPIO.HIGH:
        print("Button was pushed!")
        # Print
        print('b')
        cam = cv2.VideoCapture(0)
        print('c')
        ret, img = cam.read()
        print('d')
        cam.release()
        print(img.shape)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        
        height, width = img.shape
        if width > height:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        print(img.shape)
        
        height, width = img.shape
        new_width = 384
        new_height = int(height * new_width / width)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        print('final', img.shape)

        #img = ImageEnhance.Contrast(img).enhance(margs.factor)
        img = cv2.equalizeHist(img)
        
        img_obj = Image.fromarray(img)
        #img_obj = img_obj.convert('1')
        
        #img = np.asarray(img)
        #print(img.shape)
        #img = 255 - np.mean(img, axis=-1)
        #img = ((img > 0) * 255).astype(np.float)
        
        
        import gfx.adalogo as adalogo
        if 1 or printer.hasPaper():    
            #height, width = img.shape
            #data = img.astype(np.uint8).flatten(order='F').tolist()
            #width, height, data = adalogo.width, adalogo.height, adalogo.data
            #print(height, width, len(data), data)
            #assert 0
            print_image(printer, img_obj, LaaT=True)
            N = 3
            if N > 0:
            	printer.feed(N)
        else:
            print('no paper')
        
