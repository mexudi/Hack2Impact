import speech_recognition as sr
import os
from gtts import gTTS

def assistaneResponse(text):
    """
    Generates a text-to-speech response for the given text using the Google Text-to-Speech API (gTTS),
    saves the generated audio to a file, and plays the audio file.

    Args:
        text (str): The text to convert to speech.

    Returns:
        None
    """
    # Print the input text to the console for logging purposes
    print(text)

    # Convert the text to speech
    myobj = gTTS(text=text, lang='en', slow=False)

    # Save the converted audio to a file
    myobj.save('assistant_response.mp3')

    # Play the converted file
    os.system('start assistant_response.mp3')