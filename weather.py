import requests
import math

def get_weather_condition(api_key, location,country_code):
    """
    Retrieves the weather condition, temperature, maximum and minimum temperature, and humidity for a given location
    using the OpenWeatherMap API.

    Args:
        api_key (str): The API key for the OpenWeatherMap API.
        location (str): The name of the location to retrieve weather data for.
        country_code (str): The two-letter country code for the location.

    Returns:
        str: A string containing the weather condition, temperature, maximum and minimum temperature, and humidity for the
        specified location.
    """
    # URL for OpenWeatherMap API with location and API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location},{country_code}&appid={api_key}"
    
    
    # Make a GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the weather condition from the API response
        weather_data = response.json()
        weather_condition = weather_data["weather"][0]["description"]
        main = weather_data['main']
        temp = math.floor(weather_data['main']['temp'] - 273.15)
        max_temp = math.floor(weather_data['main']['temp_max'] - 273.15)
        min_temp = math.floor(weather_data['main']['temp_min'] - 273.15)
        humidity = weather_data['main']['humidity']

        # Return a string containing the weather condition, temperature, maximum and minimum temperature, and humidity for the specified location
        return f"The weather condition in {location} is {weather_condition}. The current temperture is {temp}, and the humidity is: {humidity}"
    else:
        # If the request was unsuccessful, return an error message
        return "Error: Unable to retrieve weather data."
