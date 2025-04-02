from RealtimeSTT import AudioToTextRecorder
import pyttsx3
import threading
from pygame import mixer
import os
import time
import random
import string

mixer.init(devicename="CABLE Input (VB-Audio Virtual Cable)")

engine = pyttsx3.init()
engine.setProperty('rate', 200)

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def speak(text):
    try:
        engine.endLoop()
    except:
        pass
    text = text.replace(",","")
    name = f"{generate_random_string()}.wav"
    engine.save_to_file(text, name)
    #engine.say(text)
    engine.runAndWait()

    mixer.music.load(name)
    mixer.music.play()
    time.sleep(10)
    mixer.music.unload()
    os.remove(name)

if __name__ == '__main__':
    print("Wait until it says 'speak now'")

    recorder = AudioToTextRecorder(language="en")

    while True:
        text = recorder.text()
        print(text)
        t = threading.Thread(target=speak, args=(text,))
        t.start()