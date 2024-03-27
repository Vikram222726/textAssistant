import speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()


def recognize_speech(display_msg):
    while True:
        try:
            print(display_msg)
            with microphone as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.1)
                audio = recognizer.listen(mic)

                text = recognizer.recognize_google(audio)
                return text.lower()
        except sr.UnknownValueError:
            print("Unknown text value, please try again")
