import os
import openai
import io
import sys

import argparse

import platform
import numpy as np
import pyaudio
import pyaudio
import wave
import pydub

from printers import Printer, DummyPrinter
import socket
import fcntl
import struct
from utils import is_rpi

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8')),
    )[20:24])

if is_rpi():
    printer = Printer()
else:
    printer = DummyPrinter()

while True:
    try:
        ip = get_ip_address('wlan0')        
        break
    except Exception:
        pass
printer.println(f'connected to {ip}')
