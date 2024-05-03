import sys
sys.path.append('src/Python-Thermal-Printer')

import argparse
from Adafruit_Thermal import *


printer = Adafruit_Thermal('/dev/ttyAMA0', 19200, timeout=5)  # must deactivate bluetooth!
#printer = Adafruit_Thermal('/dev/serial0', 19200, timeout=5)  # must deactivate bluetooth!

# Parser and settings.
parser = argparse.ArgumentParser(prefix_chars='--')
parser.add_argument('--msg', type=str)
margs = parser.parse_args()

print('aaa')

# Print
if printer.hasPaper():
    printer.println(margs.msg)
    N = 3
    printer.feed(N)
else:
    print('no paper')

