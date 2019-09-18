from inkyWeatherFun.ttf import *
import os

cwd = os.getcwd()
icon_id = "804"
sys_pod = "d"
xml = cwd + "/fonts/values/weathericons.xml"

ico_name = ttfIcon_from_iconId(icon_id, sys_pod, xml)

print(ico_name)


