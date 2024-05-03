import os
import argparse
import datetime

import math
import numpy as np
from printers import Printer


printer = Printer(mode='image')

# Parser and settings.
parser = argparse.ArgumentParser(prefix_chars='--')
parser.add_argument('--filedir', type=str)
parser.add_argument('--upper_msg', default=None, type=str)
parser.add_argument('--lower_msg', default=None, type=str)
margs = parser.parse_args()

# Print
from PIL import Image, ImageEnhance
#import numpy as np

import files

#filedirs = files.get_filedirs(margs.path)
filedirs = [margs.filedir]
for filedir in filedirs:
    print(filedir)
    img = Image.open(filedir).convert('L')
    width, height = img.size
    if width > height:
        img = img.transpose(Image.TRANSPOSE)
        pass

    width, height = img.size
    new_width = 384
    new_height = int(height * new_width / width)
    img = img.resize((new_width, new_height))
    img = ImageEnhance.Contrast(img).enhance(0.9)
    img = ImageEnhance.Brightness(img).enhance(1.2)
    
    #img = np.array(img)
    #print(img.shape)
    #img = np.clip(img, 20, None)
    #img = Image.fromarray(img)
    
    img = img.convert('1')

    import gfx.adalogo as adalogo
    if printer.has_paper():    
        #height, width = img.shape
        #data = img.astype(np.uint8).flatten(order='F').tolist()
        #width, height, data = adalogo.width, adalogo.height, adalogo.data
        #print(height, width, len(data), data)
        #assert 0
        if margs.upper_msg is not None:
            printer.println(margs.upper_msg, n=0, mode='C')
        printer.print_image(img)
        if margs.lower_msg is not None:
            printer.println(margs.lower_msg, n=0, mode='C')
            
        N = 3
        if N > 0:
            printer.feed(N)
    else:
        print('no paper')

