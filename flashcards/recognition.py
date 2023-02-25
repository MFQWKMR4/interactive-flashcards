import speech_recognition as sr


class AudioInput:
    def __init__(self):
        # create a recognizer instance
        self.r = sr.Recognizer()

    def run(self):
        # use microphone as source
        with sr.Microphone() as source:
            print("( ´ゝ`) Speak ...)")
            # adjust for ambient noise
            self.r.adjust_for_ambient_noise(source)
            # listen for audio input
            audio = self.r.listen(source)

        text = "no input"
        try:
            # recognize speech using Google Speech Recognition
            text = self.r.recognize_google(audio, language='en-US')
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}")
        return text
