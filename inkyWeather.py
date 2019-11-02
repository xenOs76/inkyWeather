#!/usr/bin/python3

### Fonts / icons
# https://erikflowers.github.io/weather-icons/
# https://openweathermap.org/weather-conditions
# https://github.com/erikflowers/weather-icons/blob/master/values/weathericons.xml

### Pillow
# https://www.programcreek.com/python/example/14029/PIL.Image.new
# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.new
# https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes


from inkyWeatherFun.ttf import *
from inkyWeatherFun.mqtt import *
from inkyWeatherFun.boxes import *
import os 
import time
import math
from datetime import datetime
from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont, ImageOps

debug = False
full_path = os.path.realpath(__file__)
wdir = os.path.dirname(full_path)

mqtt_srv = "192.168.0.101"
mqtt_forecast_topic = "forecast"
mqtt_weather_topic = "weather"
mqtt_sTemp_topic = "room-temperature"
mqtt_sHum_topic = "room-humidity"

weather_json = get_json_by_mqtt(mqtt_srv, mqtt_weather_topic)
fcast_json = get_json_by_mqtt(mqtt_srv, mqtt_forecast_topic)

clockFont = ImageFont.truetype( wdir + "/fonts/Ubuntu Nerd Font Complete.ttf",28)
dateFont = ImageFont.truetype( wdir + "/fonts/Ubuntu Nerd Font Complete.ttf",11)
wCityFont = ImageFont.truetype( wdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
wIcoFont = ImageFont.truetype( wdir + "/fonts/weathericons-regular-webfont.ttf", 30)
wDetFont = ImageFont.truetype( wdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
wTempFont = ImageFont.truetype( wdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 20)
wHumFont = ImageFont.truetype( wdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 20)
sIcoFont = ImageFont.truetype( wdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 20)
sTempFont = ImageFont.truetype( wdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
sHumFont = ImageFont.truetype( wdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
fBoxFont = ImageFont.truetype( wdir + "/fonts/Ubuntu Nerd Font Complete.ttf", 11)
fBoxWiFont = ImageFont.truetype( wdir + "/fonts/weathericons-regular-webfont.ttf", 20)

wiXmlMap = wdir + "/fonts/values/weathericons.xml"

inky_display = InkyPHAT("red")
iWhite = inky_display.WHITE 
iBlack = inky_display.BLACK
iRed = inky_display.RED
inky_display.set_border(iBlack)

wx0 = 0
hx0 = 0
wx1 = inky_display.WIDTH
hx1 = inky_display.HEIGHT

# 180° roatated display
w_wx0 = 0 		# current weather area: start width
w_hx0 = 0 		# current weather area: start heigth
w_wx1 = wx1  		# current weather area: end width
w_hx1 = int(hx1 / 2)  	# current weather area: end heigth

f_wx0 = 0 		# forecast area: start width
f_hx0 = w_hx1 		# forecast area: start heigth
f_wx1 = wx1 		# forecast area: end width
f_hx1 = int(hx1 / 2) 	# forecast area: end heigth

fBox_rows = 2
fBox_cols = 3
fBox_wx1 = math.floor(w_wx1/fBox_cols)	
fBox_hx1 = math.floor(f_hx1/fBox_rows)

print("Display width {}, height {}".format(wx1, hx1)) if debug else None
print("forecast box fBox_wx1 {}, fBox_hx1 {}".format(fBox_wx1, fBox_hx1)) if debug else None

img = Image.new("P", (wx1, hx1), color=iWhite)
draw = ImageDraw.Draw(img)

# clock 
hours = datetime.now().strftime('%H:%M')
date = datetime.now().strftime('%a, %b %d')

hour_wsize, hour_hsize = draw.textsize(hours, clockFont)
hour_wx0 = 5
hour_hx0 = 0
hour_wx1 = hour_wx0 + hour_wsize
hour_hx1 = hour_hx0 + hour_hsize

date_wsize, date_hsize = draw.textsize(date, dateFont)
date_wx0 = 5 # consider padding?
date_hx0 = hour_hx1
date_wx1 = date_wx0 + date_wsize
date_hx1 = date_hx0 + date_hsize

#draw.rectangle([(hour_wx0, hour_hx0), (hour_wx1, hour_hx1)], fill=iWhite)
draw.text((hour_wx0, hour_hx0), hours, iBlack, font=clockFont)

#draw.rectangle([(date_wx0, date_hx0), (date_wx1, date_hx1)], fill=iWhite)
draw.text((date_wx0, date_hx0), date, iBlack, font=dateFont)

# current weather
weather = json.loads(weather_json)
wCity = weather['location']
wTemp = weather['tempc']
wHum = weather['humidity']
wDet = weather['weather']
wIcoCode = weather['icon']
print("city: {}: temp {}°C, humidity {}%, {} ({})\n\n".format(wCity, wTemp, wHum, wDet, wIcoCode)) if debug else None


wCity_wsize, wCity_hsize = draw.textsize(wCity, wCityFont)
wCity_wx0 = date_wx0 # define padding?
wCity_hx0 = date_hx1
wCity_wx1 = wCity_wx0 + wCity_wsize
wCity_hx1 = wCity_hx0 + wCity_hsize
draw.text((wCity_wx0, wCity_hx0), wCity, iBlack, font=wCityFont)

wIcoUnicode = ttfUnicode_from_icon(wIcoCode, wiXmlMap)
wIco_wsize, wIco_hsize = draw.textsize(wIcoUnicode, wIcoFont)
wIco_wx0 = hour_wx1 + 5 # define padding?
wIco_hx0 = hour_hx0
wIco_wx1 = wIco_wx0 + wIco_wsize
wIco_hx1 = wIco_hx0 + wIco_hsize
draw.text((wIco_wx0, wIco_hx0), wIcoUnicode, iBlack, font=wIcoFont)

wDet_wsize, wDet_hsize = draw.textsize(wDet, wDetFont)
wDet_wx0 = wIco_wx0
wDet_hx0 = wIco_hx1
wDet_wx1 = wIco_wx0 + wDet_wsize
wDet_hx1 = wDet_hx0 + wDet_hsize
draw.text((wDet_wx0, wDet_hx0), wDet, iBlack, font=wDetFont)

wTemp = str(math.ceil(wTemp)) + "°C"
wTemp_wsize, wTemp_hsize = draw.textsize(wTemp, wTempFont)

wHum = str(wHum) + "%"
wHum_wsize, wHum_hsize = draw.textsize(wHum, wHumFont)

# padding wValCol (temp and hum): half the space left between icon column and right border
wValColPadd_wx0 = max(wIco_wx1, wDet_wx1)
wValColPadd_wsize = int((w_wx1 - wValColPadd_wx0)/2)

wTempPadd_w = int(((wValColPadd_wsize - wTemp_wsize)/2))
wTemp_wx0 = wValColPadd_wx0 + wTempPadd_w
wTemp_hx0 = 5 # define padding?
wTemp_wx1 = wTemp_wx0 + wTemp_wsize
wTemp_hx1 = wTemp_hx0 + wTemp_hsize
draw.text((wTemp_wx0, wTemp_hx0), wTemp, iBlack, font=wTempFont)

wHumPadd_w = int(((wValColPadd_wsize - wHum_wsize)/2))
wHum_wx0 = wValColPadd_wx0 + wHumPadd_w
wHum_hx0 = wTemp_hx1
wHum_wx1 = wHum_wx0 + wHum_wsize
wHum_hx1 = wHum_hx0 + wHum_hsize
draw.text((wHum_wx0, wHum_hx0), wHum, iBlack, font=wHumFont)

# sensor data
sIco = '\uf7db'
sIco_wsize, sIco_hsize = draw.textsize(sIco, sIcoFont)
sIcoPadd_wx0 = max(wTemp_wx1, wHum_wx1)
sIcoPadd_w = int(((w_wx1 - sIcoPadd_wx0) - sIco_wsize)/2)
sIco_wx0 = wTemp_wx1 + sIcoPadd_w
sIco_hx0 = wTemp_hx0
sIco_wx1 = sIco_wx0 + sIco_wsize
sIco_hx1 = sIco_hx0 + sIco_hsize
draw.text((sIco_wx0, sIco_hx0), sIco, iBlack, font=sIcoFont)

sTemp = get_sensor_value_by_mqtt(mqtt_srv, mqtt_sTemp_topic)
sTemp = str(sTemp) + "°C"
sTemp_wsize, sTemp_hsize = draw.textsize(sTemp, sTempFont)
sTempPadd_wx0 = max(wTemp_wx1, wHum_wx1)
sTempPadd_w = int(((w_wx1 - sIcoPadd_wx0) - sIco_wsize)/2)
sTemp_wx0 = wTemp_wx1 + sTempPadd_w
sTemp_hx0 = sIco_hx1
sTemp_wx1 = sTemp_wx0 + sTemp_wsize
sTemp_hx1 = sTemp_hx0 + sTemp_hsize
draw.text((sTemp_wx0, sTemp_hx0), sTemp, iBlack, font=sTempFont)

sHum = get_sensor_value_by_mqtt(mqtt_srv, mqtt_sHum_topic)
sHum = str(sHum) + "%"
sHum_wsize, sHum_hsize = draw.textsize(sHum, sHumFont)
sHumPadd_wx0 = max(wTemp_wx1, wHum_wx1)
sHumPadd_w = int(((w_wx1 - sIcoPadd_wx0) - sIco_wsize)/2)
sHum_wx0 = wTemp_wx1 + sHumPadd_w
sHum_hx0 = sTemp_hx1
sHum_wx1 = sHum_wx0 + sHum_wsize
sHum_hx1 = sHum_hx0 + sHum_hsize
draw.text((sHum_wx0, sHum_hx0), sHum, iBlack, font=sHumFont)


sHum = get_sensor_value_by_mqtt(mqtt_srv, mqtt_sHum_topic) if debug else None
print("Sensor data: temp {}, humidity {}".format(sTemp, sHum)) if debug else None

# begin of Forecast boxes
for cfBox_col in range(fBox_cols):
	for cfBox_row in range(fBox_rows):

		cfBox_pos = (cfBox_row * fBox_cols) + ( cfBox_col )
		cfBox_data = get_owslot_dict( fcast_json, (cfBox_pos+1))

		# current forecast box boundaries
		cfBox_wx0 = f_wx0 + (cfBox_col * fBox_wx1)
		cfBox_hx0 = f_hx0 + (cfBox_row * fBox_hx1)
		cfBox_wx1 = cfBox_wx0 + fBox_wx1
		cfBox_hx1 = cfBox_hx0 + fBox_hx1
		draw.rectangle([(cfBox_wx0, cfBox_hx0), (cfBox_wx1, cfBox_hx1)], iWhite, 1) 		# outer border
		draw.line([(cfBox_wx1, cfBox_hx0),(cfBox_wx1, cfBox_hx1)], fill=iBlack, width=1) 	# right border
		draw.line([(cfBox_wx0, cfBox_hx1),(cfBox_wx1, cfBox_hx1)], fill=iBlack, width=1) 	# lower border
		#print("forecast box position {}, c {} / r {}: w0 {}, w1 {}, h0 {}, h1 {} ".format(cfBox_pos, cfBox_col, cfBox_row, cfBox_wx0, cfBox_wx1, cfBox_hx0,  cfBox_hx1))	

		# current forecast box content
		cfBoxWi = ttfUnicode_from_iconId(cfBox_data['iconId'], cfBox_data['pod'], wiXmlMap)
		cfBoxHour = cfBox_data['time']
		cfBoxTemp = cfBox_data['temp']

		# text size
		cfBoxWi_w, cfBoxWi_h = fBoxWiFont.getsize(cfBoxWi)
		cfBoxHour_w, cfBoxHour_h = fBoxFont.getsize(cfBoxHour)
		cfBoxTemp_w, cfBoxTemp_h = fBoxFont.getsize(cfBoxTemp)
		cfBoxWiHalfPadding = (fBox_wx1 - (cfBoxWi_w + cfBoxTemp_w))/2

		# print weather icon
		#print("forecast weather icon size: width {}, height {}".format(cfBoxWi_w, cfBoxWi_h))	
		cfBoxWi_rel_wx0 = cfBox_wx0 + int((cfBoxWiHalfPadding/2))
		cfBoxWi_rel_hx0 = cfBox_hx0
		draw.text((cfBoxWi_rel_wx0, cfBoxWi_rel_hx0), cfBoxWi, iBlack, font=fBoxWiFont)

		# print box's hour
		#print("forecast hour text size: width {}, height {}".format(cfBoxHour_w, cfBoxHour_h))	
		cfBoxHour_rel_wx0 = cfBoxWi_rel_wx0 + cfBoxWi_h + int((cfBoxWiHalfPadding/2))
		cfBoxHour_rel_hx0 = cfBox_hx0
		draw.text((cfBoxHour_rel_wx0, cfBoxHour_rel_hx0), cfBoxHour, iBlack, font=fBoxFont)

		# print temp
		#print("forecast temp text size: width {}, height {}".format(cfBoxTemp_w, cfBoxTemp_h))	
		cfBoxTemp_rel_wx0 = cfBoxWi_rel_wx0 + cfBoxWi_h + int((cfBoxWiHalfPadding/2))
		cfBoxTemp_rel_hx0 = cfBox_hx0 + cfBoxHour_h
		draw.text((cfBoxTemp_rel_wx0, cfBoxTemp_rel_hx0), cfBoxTemp, iBlack, font=fBoxFont)


img_trans = img.transpose(Image.ROTATE_180)
inky_display.set_image(img_trans)
inky_display.show()
