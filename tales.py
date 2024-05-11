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

import random

from printers import Printer, DummyPrinter
from utils import is_rpi


def _find_audio_device(name):
    p = pyaudio.PyAudio()
    for idx in range(p.get_device_count()):
        audio_device = p.get_device_info_by_index(idx)
        if audio_device['name'].startswith(name):
            info = {
                'name': name,
                'sample_rate': int(audio_device['defaultSampleRate']),
            }
            return idx, info
    return None, {}


def find_audio_device(names):
    for name in names:
        idx, info = _find_audio_device(name)
        if idx is not None:
            return idx, info
    return None, {}


def get_audio_device_names():
    p = pyaudio.PyAudio()
    audio_device_names = []
    for idx in range(p.get_device_count()):
        audio_device = p.get_device_info_by_index(idx)
        audio_device_names.append(audio_device['name'])
    return audio_device_names


from files import load_json

print(get_audio_device_names())
openai.api_key = load_json("config.json")["api_key"]
openai.api_requestor.TIMEOUT_SECS = 60
openai.api_requestor.MAX_CONNECTION_RETRIES = 1

dev_index, info = find_audio_device([
    'USB PnP Sound Device: Audio',
    'GENERAL WEBCAM: USB Audio',
    'default',
])
print(info)
sample_rate = info['sample_rate']
audio_format = pyaudio.paInt16  # resolution
channels = 1
chunk = 8192
record_secs = 10
wav_output_filename = 'audio.wav' # name of .wav file



import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8')),
    )[20:24])


if is_rpi():
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library


BUTTON_GPIO = 16

if is_rpi():
    printer = Printer()
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
else:
    printer = DummyPrinter()


printer.println("ready!")

while True: # Run forever
    cond = 1
    if is_rpi():
        cond = GPIO.input(BUTTON_GPIO) == GPIO.HIGH

    if cond:
        try:
            audio = pyaudio.PyAudio() # create pyaudio instantiation
            # create pyaudio stream
            stream = audio.open(format=audio_format,
                                rate=sample_rate,
                                channels=channels,
                                input_device_index=dev_index,
                                input=True,
                                frames_per_buffer=chunk,
                                )
            printer.println('recording ...')
            frames = []

            # loop through stream and append audio chunks to frame array
            # for _ in range(int((sample_rate / chunk) * record_secs)):
            while True:
                data = stream.read(chunk, exception_on_overflow=False)
                frames.append(data)
                if is_rpi():
                    cond = GPIO.input(BUTTON_GPIO) == GPIO.LOW
                else:
                    cond = 1
                record_secs = len(frames) / (sample_rate / chunk)
                if cond and record_secs > 3:
                    break
            printer.println(f'finished recording: {record_secs:.3f} secs')

            # stop the stream, close it, and terminate the pyaudio instantiation
            stream.stop_stream()
            stream.close()
            audio.terminate()

            # xxx
            audio_file_container = io.BytesIO()
            sound = pydub.AudioSegment(b''.join(frames), sample_width=2, channels=channels, frame_rate=sample_rate)
            sound.low_pass_filter(10000)
            if not is_rpi():
                sound.export('./tmp/audio.mp3', format='mp3')
            sound.export(audio_file_container, format='mp3')
            audio_file_container.seek(0)
            audio_file_container.name = 'audio.mp3'

        except Exception as e:
            printer.println(f'error audio: {e}')
            continue

        try:
            audio_file = io.BufferedReader(audio_file_container)
            transcript = openai.Audio.transcribe('whisper-1', audio_file)
            text = transcript.text
            print(text)
            # printer.println(text)

        except Exception as e:
            printer.println(f'error whisper: {e}')
            continue
	
        categories = ["fantasía", "misterio", "terror", "romance"]
        try:
            messages = []
            cat = random.choice(categories)
            words = text.lower().replace(".", "").replace(",", "").replace(" ", ", ")
            content =  f"crea un cuento de {cat} y de tres parrafos. El cuento debe estar basado en las siguientes palabras: {words}"
            messages.append({"role": "user", "content": content})
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            text = response.choices[0].message.content
            printer.println(f"category: {cat}", n=0)
            printer.println(f"keywords: {words}", n=0)
            printer.print_line()
            printer.println(text)

        except Exception as e:
            printer.println(f'error gpt: {e}')
            continue


