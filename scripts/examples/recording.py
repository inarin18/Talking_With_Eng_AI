"""PyAudio Example: Record a few seconds of audio and save to a wave file."""

import wave
import sys

import pyaudio
import speech_recognition as sr

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

with wave.open('sounds/output.wav', 'wb') as wf:
    p = pyaudio.PyAudio()
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

    print('Recording...')
    for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        
        in_data = stream.read(CHUNK)
        
        wf.writeframes(in_data)
        
        global sprec 
        # speech recogniserインスタンスを生成
        sprec = sr.Recognizer() 

        try:
            audiodata  = sr.AudioData(in_data, RATE, 2)
            sprec_text = sprec.recognize_google(audiodata, language='eng')
            print(sprec_text)
        
        except :
            pass
        
        
    print('Done')

    stream.close()
    p.terminate()