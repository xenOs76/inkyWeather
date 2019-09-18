

ow_iconId_map = {}

# Group 2xx: Thunderstorm
ow_iconId_map["11d"] = {"id":"200", "pod":"d"}

# Group 3xx: Drizzle
ow_iconId_map["09d"]  = {"id":"300", "pod":"d"}

# Group 5xx: Rain
ow_iconId_map["10d"] = "500"
ow_iconId_map["13d"] = "501"
ow_iconId_map["09d"] = "511"


print(ow_iconId_map)
print(ow_iconId_map["11d"]["id"])
