from RealtimeSTT import AudioToTextRecorder
import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 250)

def speak(text):
    try:
        engine.endLoop()
    except:
        pass
    text = text.replace(",","")
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    print("Wait until it says 'speak now'")

    recorder = AudioToTextRecorder()

    while True:
        text = recorder.text()
        print(text)
        t = threading.Thread(target=speak, args=(text,))
        t.start()