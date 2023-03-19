import speech_recognition as sr
import re
from weather import get_weather_condition
from text_to_speech import assistaneResponse
import weather_api


api_key = weather_api.api_key
location = weather_api.location
country_code = weather_api.country_code


# Create a recognizer object
r = sr.Recognizer()

assistaneResponse("Hello, How Can Help you today")
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


word_to_search = "weather"
word_to_search_2 = "describe"
word_to_search_3 = "color"
# Using the search() function to find the word in the text
match = re.search(word_to_search, text, re.IGNORECASE)
match_2 = re.search(word_to_search_2, text, re.IGNORECASE)
match_3 = re.search(word_to_search_3, text, re.IGNORECASE)
if match:
    weather_condition = get_weather_condition(api_key, location,country_code)
    assistaneResponse(weather_condition)
    #print(f"'{word_to_search}' found in the text.")
elif match_2:
    from image_caption import predict_step
    caption = predict_step(['image-captioning-example.png'])
    assistaneResponse(caption[0])
elif match_3:
    from colors_detection import color_detection
    color_detection()
else:
    print(f"'{word_to_search}' not found in the text.")