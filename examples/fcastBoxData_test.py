from inkyWeatherFun.ttf import *
from inkyWeatherFun.mqtt import *
from inkyWeatherFun.boxes import *

import json
import datetime


mqtt_srv = "192.168.0.101"
mqtt_forecast_topic = "forecast"
mqtt_weather_topic = "weather"

weather_json = get_weather_json_by_mqtt(mqtt_srv, mqtt_weather_topic)
fcast_json = get_forecast_json_by_mqtt(mqtt_srv, mqtt_forecast_topic)


def get_fBox_data(fcast_json, fslot):

	fBox = {}
	fJson = json.loads(fcast_json)
	fSlot = fJson['list'][fslot]
	temp = int(fSlot['main']['temp'])
	dt = datetime.datetime.utcfromtimestamp(fSlot['dt'])

	fBox['temp'] = str(temp) + "°C"
	fBox['iconId'] = fSlot['weather'][0]['id']
	fBox['pod'] = str(fSlot['sys']['pod'])
	fBox['time'] = dt.strftime("%H:%M")
	return fBox

slot1 = get_fBox_data(fcast_json, 1)

print(slot1)
