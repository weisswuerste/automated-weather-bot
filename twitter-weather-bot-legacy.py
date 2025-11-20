# -*- coding: utf-8 -*-
#!/usr/bin/python3.8

import requests
import tweepy
from datetime import date

user_key = ''
user_secret = ''

access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(user_key, user_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def APIs():
    API_key = ''
    base_url = "http://api.openweathermap.org/data/2.5/onecall?"
    
    lat = '41.3640154'
    lon = '2.1587383'
    ##### Barcelona's location is chosen here.
    
    exclude = 'minutely,hourly,alerts'
    final_url_english = base_url + "lat=" + lat + "&lon=" + lon + "&exclude=" + exclude + "&appid=" + API_key + "&units=metric"
    final_url_spanish = base_url + "lat=" + lat + "&lon=" + lon + "&exclude=" + exclude + "&appid=" + API_key + "&units=metric" + "&lang=es"
    weather_data_english, weather_data_spanish = requests.get(final_url_english).json(), requests.get(final_url_spanish).json()
    
    return weather_data_english, weather_data_spanish

def weather(weather_data_english, weather_data_spanish):
    temp = weather_data_english['current']['temp']
    feels_like = weather_data_english['current']['feels_like']
    temp_min = weather_data_english['daily'][0]['temp']['min']
    temp_max = weather_data_english['daily'][0]['temp']['max']
    climate_english = weather_data_english['daily'][0]['weather'][0]['description']
    climate_spanish = weather_data_spanish['daily'][0]['weather'][0]['description']
    
    return temp, feels_like, temp_min, temp_max, climate_english, climate_spanish

def dates():
    months_spanish = ['Meses', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    months_english = ['Months', 'January', 'February', 'March', 'April', 'May', 'June', 'June', 'August', 'September', 'October', 'November', 'December']

    day = date.today().day
    month = date.today().month
    year = date.today().year
    
    return months_spanish, months_english, day, month, year

def tweeting_spanish(months_spanish, day, month, year, temp, feels_like, temp_min, temp_max, climate_spanish):
    tweet_spanish = f'¿Cómo os va? \nEs {day} de {months_spanish[month]} de {year}. ¿Y cuál es el clima el día de hoy? \n\nNos encontramos con temperaturas de {temp}°C, pero se siente como {feels_like}°C. Por el día de hoy la temperatura máxima y mínima son {temp_max}°C y {temp_min}°C. \n\nEl clima también nos brinda {climate_spanish}.'
    api.update_status(status=tweet_spanish)

def tweeting_english(months_english, day, month, year, temp, feels_like, temp_min, temp_max, climate_english):
    tweet_english = f'How are all of you? \nIt is {day} {months_english[month]} {year}, and what is the weather like today? \n\nWe are seeing {temp}°C, but it feels like {feels_like}°C. The high/low temperatures today are {temp_max}°C and {temp_min}°C. \n\nThe weather is also giving us {climate_english}.'
    api.update_status(status=tweet_english)

def main():
    weather_data_english, final_url_spanish = APIs()
    temp, feels_like, temp_min, temp_max, climate_english, climate_spanish = weather(weather_data_english, final_url_spanish)
    months_spanish, months_english, day, month, year = dates()
    tweeting_spanish(months_spanish, day, month, year, temp, feels_like, temp_min, temp_max, climate_spanish)
    tweeting_english(months_english, day, month, year, temp, feels_like, temp_min, temp_max, climate_english)

if __name__ == "__main__":
    main()
