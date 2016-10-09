from flask import Flask, request, send_from_directory, send_file
##

from src.TimeStamp import TimeStamp
from src.editor import *
import os, wave,pickle,random
import re
import pydub import AudioSegment
import markovify

##
from generate_speech_to_audio.py import S2A
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_folder='client/build/', static_url_path='')


@app.route('/')
def root():
    print("Hello World!")
    return app.send_static_file("index.html")

def gen_audio(person, text):
    #person: 'trump', 'hillary', or 'obama'
    output = wave.open("sample-o.wav", "wb")
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(16000)
    s = S2A(person)
    s.speech_to_audio(text,output)
    output.close()
    AudioSegment.from_wav("sample-o.wav").export("sample-o.mp3", format="mp3")
    try:
	return send_file('sample-o.mp3', attachment_filename='sample-o.mp3')
    except Exception as e:
	return str(e)
    
def gen_phrase(person):
    #markov shit
    s = S2A(person)
    return s.text_model.make_short_sentence(200)
    

if __name__ == "__main__":
    app.run()
