import pyttsx3


def play_voice(words):
    engine = pyttsx3.init()
    a = engine.say(words)
    engine.runAndWait()
    engine.stop()


if __name__ == '__main__':
    play_voice('阿巴阿巴')
