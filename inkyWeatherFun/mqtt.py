#!/usr/bin/python3

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

def get_json_by_mqtt(mqtt_srv, mqtt_json_topic):
	json_msg = subscribe.simple(mqtt_json_topic, msg_count=1, hostname=mqtt_srv, retained=True, keepalive=3)
	return json_msg.payload.decode('utf-8')

def get_sensor_value_by_mqtt(mqtt_srv, mqtt_sensor_topic):
	sensor_msg = subscribe.simple(mqtt_sensor_topic, msg_count=1, hostname=mqtt_srv, retained=True, keepalive=3)
	return int(sensor_msg.payload)

