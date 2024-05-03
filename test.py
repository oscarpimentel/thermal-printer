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
from utils import is_rpi

if is_rpi():
    printer = Printer()
else:
    printer = DummyPrinter()

printer.println("testing ...")
printer.print_line()

