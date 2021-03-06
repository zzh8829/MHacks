#!/usr/bin/env python
from os import environ, path
import os,sys
import shutil
import pickle

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from moviepy.editor import *

from pocketsphinx import Pocketsphinx, get_model_path, get_data_path, AudioFile

model_path = get_model_path()

if len(sys.argv) < 2:
    sys.exit(0)

name = sys.argv[-1]

print(name)

file = "speech/%s.wav"%name
#file = "firework2.wav"
#file = "test2.wav"

config = {
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'dict': os.path.join(model_path, 'cmudict-en-us.dict'),
    'audio_file': file,
    'buffer_size': 1024,
    'no_search': False,
    'full_utt': False,
}

words = {}

def proc_segs(segs):
  for seg in segs:
    #print(seg.start_frame, seg.end_frame, seg.word)
    print(seg)

    word, acc, start, end = seg

    word = word.split('(')[0]

    if word.isalpha():
      if not word in words:
        words[word] = []
      words[word].append(seg)

audio = AudioFile(**config)
for phrase in audio:
    print(phrase)
    proc_segs(phrase.segments(detailed=True))

#proc_segs(ps.segments(detailed=True))

clip = AudioFileClip(file)

import wave
origAudio = wave.open(file,'rb')
frameRate = origAudio.getframerate()
nChannels = origAudio.getnchannels()
sampWidth = origAudio.getsampwidth()

print(origAudio.getparams())

os.makedirs('speech/%s'%name,exist_ok=True)
#shutil.rmtree('speech/%s/'%, ignore_errors=True)

with open('speech/%s.pickle'%name, 'wb') as f:
  pickle.dump(words, f)

for word in words:
  for i in range(len(words[word])):
    seg = words[word][i]
    _, acc, start, end = seg

    os.makedirs('speech/%s/%s'%(name, word),exist_ok=True)

    segname = "speech/%s/%s/%d.wav"%(name, word,i)

    origAudio.setpos((start) * 160)
    chunkData = origAudio.readframes((end - start) * 160)

    chunkAudio = wave.open(segname,'wb')
    chunkAudio.setnchannels(nChannels)
    chunkAudio.setsampwidth(sampWidth)
    chunkAudio.setframerate(frameRate)
    chunkAudio.writeframes(chunkData)
    chunkAudio.close()


# print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
