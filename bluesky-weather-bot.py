# -*- coding: utf-8 -*-
#!/usr/bin/python3.8

import requests
from datetime import datetime, timezone, timedelta
from atproto import Client

def weatherAPIAccess():
    API_key = ''
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    
    lat = '47.7144788'
    lon = '11.7529066'
    ##### Tegernsee's location is chosen here.

    exclude = 'minutely,hourly,alerts'
    final_url = base_url + "lat=" + lat + "&lon=" + lon + "&exclude=" + exclude + "&appid=" + API_key + "&units=metric" + "&lang=de"
    weather_data = requests.get(final_url).json()

    return weather_data

def weatherMetadata(weather_data):
    temp = round(weather_data['main']['temp'], 1)
    feels_like = round(weather_data['main']['feels_like'], 1)
    sunrise = weather_data['sys']['sunrise']
    sunset = weather_data['sys']['sunset']
    climate = weather_data['weather'][0]['description']

    return temp, feels_like, sunrise, sunset, climate

def timeAdjustments(sunrise, sunset):
    offset = timedelta(hours=1)
    sunrise_offset = datetime.fromtimestamp(int(sunrise), tz=timezone.utc) + offset
    sunset_offset = datetime.fromtimestamp(int(sunset), tz=timezone.utc) + offset

    date = datetime.strftime(sunrise_offset, '%Y-%m-%d')
    sunrise_local = datetime.strftime(sunrise_offset, '%H:%M:%S')
    sunset_local = datetime.strftime(sunset_offset, '%H:%M:%S')

    return date, sunrise_local, sunset_local

def postToBsky(date, sunrise_local, temp, feels_like, climate, sunset_local):
    bsky_post = f'Servus aus Tegernsee! \n\nHeute is {date}, und der Sonnenaufgang war ungefähr {sunrise_local}. Während ist der Temperatur {temp}°C draußen, fühlt sich an wie {feels_like}°C. \n\nFür den Rest des Tages haben Wir {climate}, und der Sonnenuntergang wird ungefähr {sunset_local}.'
    
    client = Client()
    client.login('', '')
    post = client.send_post(bsky_post)
    post.uri
    post.cid

def main():
    weather_data = weatherAPIAccess()
    temp, feels_like, sunrise, sunset, climate = weatherMetadata(weather_data)
    date, sunrise_local, sunset_local = timeAdjustments(sunrise, sunset)
    postToBsky(date, sunrise_local, temp, feels_like, climate, sunset_local)

if __name__ == "__main__":
    main()
