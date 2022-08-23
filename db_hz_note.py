import librosa
import pyaudio
import numpy as np
from math import log10

CHUNK = 1024  # number of data points to read at a time
RATE = 44100  # time resolution of the recording device (Hz)
DEVICE = 1  # default
db = 0

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                input_device_index=int(input("введите устройство: ")),
                frames_per_buffer=CHUNK)

while True:
    indata = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    audio_data = np.fromstring(indata, dtype=np.short)
    if audio_data[1] > 0:
        db = 20 * log10(audio_data[1])
        db = int(db)
        # Take the fft and square each value
        fftData = abs(np.fft.rfft(indata)) ** 2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which + x1) * RATE / CHUNK
            if thefreq > 1700 or thefreq < 70:
                continue
            else:
                print(db, end='')
                print('Db', end=' ')
                print(int(thefreq), end='')
                print('Hz', end=' ')
                print(librosa.hz_to_note(thefreq))
        else:
            thefreq = which * RATE / CHUNK
            if thefreq > 1700 or thefreq < 70:
                continue
            else:
                print(db, end='')
                print('Db', end=' ')
                print(int(thefreq), end='')
                print('Hz', end=' ')
                print(librosa.hz_to_note(thefreq))
    else:
        continue

stream.close()
p.terminate()


