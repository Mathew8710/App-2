import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate

# Select female voice if available
voices = engine.getProperty('voices')
for voice in voices:
    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    engine.say(text)
    engine.runAndWait()
