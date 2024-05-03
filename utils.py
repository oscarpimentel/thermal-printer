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

def is_rpi():
    return 'armv' in platform.platform()

