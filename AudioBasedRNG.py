from sys import byteorder
from array import array
from struct import pack
from datetime import datetime
from sys import argv

import pyaudio
import random

try:
    numOfFrames = int(argv[1])
except IndexError:
    numOfFrames = 1025 # Default value

# I stole this from StackOverflow so, I have no idea about how the intricacies of this method work. All I know is it records audio.
def record(frames = 1) -> str:
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100,
        input=True,
        frames_per_buffer=1024)
    try:
        return stream.read(frames, False)    
    finally:
        stream.close()
    

def generateSeed(frames = 1) -> int:
    audioData = record(frames)
    seed = 0
    for i in audioData:
        seed += i
    
    # This is where the manipulation of the audio data to make it into a seed
    seed /= len(audioData)
    seed *= datetime.now().timestamp()
    if str(seed).count(".") == 1:
        arr = str(seed).split(".")
        seed = int(arr[0] + arr[1])
    
    return seed

def newRNG(frames = 1) -> random:
    rng = random
    rng.seed(generateSeed(frames))
    return rng

