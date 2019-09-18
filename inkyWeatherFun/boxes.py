
import json
import datetime
import math

def get_owslot_dict(fcast_json, fslot):

        fBox = {}
        fJson = json.loads(fcast_json)
        fSlot = fJson['list'][fslot]
        temp = math.ceil(fSlot['main']['temp'])
        hum = math.ceil(fSlot['main']['humidity'])
        dt = datetime.datetime.utcfromtimestamp(fSlot['dt'])

        fBox['temp'] = str(temp) + "°C"
        fBox['hum'] = str(hum) + "%"
        fBox['iconId'] = str(fSlot['weather'][0]['id'])
        fBox['pod'] = str(fSlot['sys']['pod'])
        fBox['time'] = dt.strftime("%H:%M")
        return fBox


