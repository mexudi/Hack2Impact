import speech_recognition as sr
import re
from weather import get_weather_condition
from text_to_speech import assistaneResponse
import weather_api

# Get the API key and location from weather_api.py
api_key = weather_api.api_key
location = weather_api.location
country_code = weather_api.country_code


# Create a recognizer object
r = sr.Recognizer()

# Say hello to the user
assistaneResponse("Hello, How Can I Help you today")

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Speak something!")
    
    # Adjust for ambient noise
    r.adjust_for_ambient_noise(source)

    # Record audio from the microphone
    audio = r.listen(source)

# Convert speech to text using Google Speech-to-Text API
try:
    text = r.recognize_google(audio)
    print(f"You said: {text}")
except sr.UnknownValueError:
    reply = 'Sorry, I could not understand what you said'
    assistaneResponse(reply)
except sr.RequestError as e:
    reply = "Request Error"
    assistaneResponse(reply)

# Define words to search for in the user's speech
word_to_search = "weather"
word_to_search_2 = "describe"
word_to_search_3 = "color"

# Using the search() function to find the word in the user's speech
match = re.search(word_to_search, text, re.IGNORECASE)
match_2 = re.search(word_to_search_2, text, re.IGNORECASE)
match_3 = re.search(word_to_search_3, text, re.IGNORECASE)

# If the word "weather" is found in the user's speech, get the weather condition and respond to the user
if match:
    weather_condition = get_weather_condition(api_key, location,country_code)
    assistaneResponse(weather_condition)

# If the word "describe" is found in the user's speech, use image captioning to describe an image and respond to the user
elif match_2:
    from image_caption import predict_step
    caption = predict_step(['images_1.jpeg'])
    assistaneResponse(caption[0])

# If the word "color" is found in the user's speech, use color detection to detect colors in an image and respond to the user
elif match_3:
    from colors_detection import color_detection
    color_detection()

# If none of the words are found in the user's speech, let the user know that the program did not understand their request
else:
    assistaneResponse("You are using an unkown key word")
    print("Error not found in the text. Unknown Key Word")