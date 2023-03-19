import speech_recognition as sr
import os
from gtts import gTTS

def assistaneResponse(text):
    print(text)

    # COnvert the text to speech
    myobj = gTTS(text=text, lang='en', slow=False)

    # Save the converted audio to a file
    myobj.save('assistant_response.mp3')

    # Play the converted file
    os.system('start assistant_response.mp3')