#!/usr/bin/python3

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json
import os
import sys

debug = True

mqtt_srv = "192.168.0.101"
mqtt_forecast_topic = "forecast"
mqtt_weather_topic = "weather"
mqtt_sTemp_topic = "room-temperature"
mqtt_sHum_topic = "room-humidity"

fcast_msg = subscribe.simple(mqtt_forecast_topic, msg_count=1, hostname=mqtt_srv, retained=True, keepalive=3)
weather_msg = subscribe.simple(mqtt_weather_topic, msg_count=1, hostname=mqtt_srv, retained=True, keepalive=3)

#print(weather_msg.payload) if debug else None
#print(fcast_msg.payload) if debug else None

forecast = json.loads(fcast_msg.payload.decode('utf-8'))
weather = json.loads(weather_msg.payload.decode('utf-8'))

city = weather['location']
temp = weather['tempc']
hum = weather['humidity']
weath = weather['detail']
wico = weather['icon']

print("Current weather - city: {}: temp {}°C, humidity {}%, {} ({})\n\n".format(city, temp, hum, weath, wico)) if debug else None


print("Forecast\n") if debug else None
city = forecast['city']['name']
country = forecast['city']['country']

fcast_lists = forecast['list']
for fci in range(len(fcast_lists)):

	temp = forecast['list'][fci]['main']['temp']
	hum = forecast['list'][fci]['main']['humidity']
	weath = forecast['list'][fci]['weather'][0]['description']
	fico = forecast['list'][fci]['weather'][0]['icon']
	time = forecast['list'][fci]['dt_txt']
	print("city: {} ({}): temp {}°C, humidity {}%, {} / {} ({})".format(city, country, temp, hum, weath, fico, time )) if debug else None


sTemp_msg = subscribe.simple(mqtt_sTemp_topic, msg_count=1, hostname=mqtt_srv, retained=True, keepalive=3)
sTemp = int(sTemp_msg.payload)
print("sTemp: {}".format(sTemp)) if debug else None
