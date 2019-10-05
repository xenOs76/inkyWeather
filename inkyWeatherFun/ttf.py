
# Mapping between OpenWeather API icon name and Weather Icons' unicode value
#
# see:
# https://erikflowers.github.io/weather-icons/api-list.html
# https://github.com/erikflowers/weather-icons/blob/master/values/weathericons.xml
# https://openweathermap.org/api
# https://openweathermap.org/current#one
# https://openweathermap.org/forecast5

from xml.dom import minidom
import html

def ttfUnicode_from_iconId(icon_id, sys_pod, xml_map):

	data = ''
	ico_name = "wi_owm_"
	if (sys_pod == 'd'): 
		ico_name += "day_";
	elif (sys_pod == 'n'):
		ico_name += "night_";
	else:
		raise ValueError('Invalid pod value')	

	ico_name += icon_id
	xml_dom = minidom.parse(xml_map)
	strings = xml_dom.getElementsByTagName('string')

	for string in strings:
		if string.attributes['name'].value == ico_name:
			value = string.firstChild.nodeValue
			data = html.unescape(value)
	return  data

def ttfUnicode_from_icon( icon,  xml_map):

	# https://openweathermap.org/weather-conditions
	ow_iconId_map = {}

	# Group 2xx: Thunderstorm
	ow_iconId_map["11d"] = {"id":"200", "pod":"d"}
	ow_iconId_map["11n"] = {"id":"200", "pod":"n"}

	# Group 3xx: Drizzle
	ow_iconId_map["09d"] = {"id":"300", "pod":"d"}

	# Group 5xx: Rain
	ow_iconId_map["10d"] = {"id":"500", "pod":"d"}
	ow_iconId_map["10n"] = {"id":"500", "pod":"n"}
	ow_iconId_map["13d"] = {"id":"501", "pod":"d"}
	ow_iconId_map["13n"] = {"id":"501", "pod":"n"}
	ow_iconId_map["09d"] = {"id":"511", "pod":"d"}
	ow_iconId_map["09n"] = {"id":"511", "pod":"n"}

	# Group 6xx: Snow
	ow_iconId_map["13d"] = {"id":"600", "pod":"d"}
	ow_iconId_map["13n"] = {"id":"600", "pod":"n"}

	# Group 7xx: Atmosphere
	ow_iconId_map["50d"] = {"id":"701", "pod":"d"}
	ow_iconId_map["50n"] = {"id":"701", "pod":"n"}

	# Group 800: Clear
	ow_iconId_map["01d"] = {"id":"800", "pod":"d"}
	ow_iconId_map["01n"] = {"id":"800", "pod":"n"}

	# Group 80x: Clouds
	ow_iconId_map["02d"] = {"id":"801", "pod":"d"}
	ow_iconId_map["02n"] = {"id":"801", "pod":"n"}
	ow_iconId_map["03d"] = {"id":"802", "pod":"d"}
	ow_iconId_map["03n"] = {"id":"802", "pod":"n"}
	#ow_iconId_map["04d"] = {"id":"803", "pod":"d"}
	#ow_iconId_map["04n"] = {"id":"803", "pod":"n"}
	ow_iconId_map["04d"] = {"id":"804", "pod":"d"}
	ow_iconId_map["04n"] = {"id":"804", "pod":"n"}


	icon_id = ow_iconId_map[icon]["id"]
	sys_pod = ow_iconId_map[icon]["pod"]	

	data = ttfUnicode_from_iconId(icon_id, sys_pod, xml_map)
	return data

