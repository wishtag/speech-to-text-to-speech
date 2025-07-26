from RealtimeSTT import AudioToTextRecorder
import pyttsx3
import threading
from pygame import mixer
import sounddevice as sd
import os
import time
import random
import string
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def list_output_devices():
    print("\nAvailable output devices:")
    devices = sd.query_devices()
    output_devices = []
    for idx, device in enumerate(devices):
        if device['max_output_channels'] > 0:
            print(f"{idx}: {device['name']}")
            output_devices.append((idx, device['name']))
    return output_devices

def select_output_device(output_devices):
    try:
        index = int(input("\nEnter the number of the output device to use: "))
        return output_devices[index][1]
    except (IndexError, ValueError):
        print("Invalid selection. Default device will be used.")
        return None

def select_speak_function(speak_options):
    print("\nAvailable speaking methods:")
    for idx, option in enumerate(speak_options):
        print(f"{idx}: {option}")
    try:
        index = int(input("Select the speaking method: "))
        selected_key = list(speak_options.keys())[index]
        return speak_options[selected_key]
    except (IndexError, ValueError):
        print("Invalid selection. Defaulting to first option.")
        return list(speak_options.values())[0]

# Setup pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 250)

# --------------------- Speak Methods -----------------------

# 1. gTTS
def speak_with_gtts(text):
    text = text.replace(",", "")
    filename = f"{generate_random_string()}.mp3"
    tts = gTTS(text=text)
    tts.save(filename)
    sound = AudioSegment.from_mp3(filename)
    play(sound)
    os.remove(filename)

# 2. pyttsx3 direct
def speak_with_pytts3(text):
    try:
        engine.endLoop()
    except:
        pass
    text = text.replace(",", "")
    engine.say(text)
    engine.runAndWait()

# 3. Original (pyttsx3 + save .wav + mixer playback)
def speak_original(text):
    try:
        engine.endLoop()
    except:
        pass
    text = text.replace(",", "")
    filename = f"{generate_random_string()}.wav"
    engine.save_to_file(text, filename)
    engine.runAndWait()

    mixer.music.load(filename)
    mixer.music.play()

    # Wait until done
    while mixer.music.get_busy():
        time.sleep(0.1)

    mixer.music.unload()
    os.remove(filename)

# ----------------------------------------------------------

if __name__ == '__main__':
    print("Wait until it says 'speak now'")

    # Select output device
    output_devices = list_output_devices()
    selected_device_name = select_output_device(output_devices)

    # Select speaking function
    speak_options = {
        "Speak with pyttsx3 (direct)": speak_with_pytts3,
        "Speak with gTTS": speak_with_gtts,
        "Speak with pyttsx3 + mixer (original)": speak_original
    }
    speak = select_speak_function(speak_options)

    # Initialize mixer
    try:
        if selected_device_name:
            mixer.init(devicename=selected_device_name)
        else:
            mixer.init()
    except Exception as e:
        print(f"Failed to initialize mixer with selected device: {e}")
        print("Falling back to default device.")
        mixer.init()

    recorder = AudioToTextRecorder(language="en")

    while True:
        text = recorder.text()
        print("You said:", text)
        t = threading.Thread(target=speak, args=(text,))
        t.start()
