from RealtimeSTT import AudioToTextRecorder
import pyttsx3
import threading

engine = pyttsx3.init()

def speak(text):
    try:
        engine.endLoop()
    except:
        pass
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder()

    while True:
        print(recorder.text())
        t = threading.Thread(target=speak, args=(recorder.text(),))
        t.start()