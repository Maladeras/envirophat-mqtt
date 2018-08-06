#!/usr/bin/env python

import time
import os
from envirophat import weather, leds, light
from influxdb import InfluxDBClient
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

influx_host = config.get('db', 'host')
port = config.getint('db', 'port')
dbname = config.get('db', 'dbname')
user = config.get('db', 'user')
password = config.get('db', 'password')

host = config.get('main', 'host')
sleep_time = config.getint('main', 'sleep')

client = InfluxDBClient(influx_host, port, user, password, dbname)
client.create_database(dbname)

def get_cpu_temp():
    path="/sys/class/thermal/thermal_zone0/temp"
    f = open(path, "r")
    temp_raw = int(f.read().strip())
    temp_cpu = float(temp_raw / 1000.0)
    return temp_cpu

def get_data_points():
    temp_cpu = get_cpu_temp()
    temperature = weather.temperature()
    pressure = round(weather.pressure(), 2)
    light_val = light.light()

    iso = time.ctime()
    json_body = [
            {
                "measurement": "ambient_celcius",
                "tags": {"host": host},
                "time": iso,
                "fields": {
                    "value": temperature,
                    "val": float(temperature)
                    }
                },
            {
                "measurement": "cpu_celcius",
                "tags": {"host": host},
                "time": iso,
                "fields": {
                    "value": temp_cpu,
                    }
                },
            {
                "measurement": "ambient_light",
                "tags": {"host": host},
                "time": iso,
                "fields": {
                    "value": light_val,
                    }
                },
            {
                "measurement": "ambient_pressure",
                "tags": {"host": host},
                "time": iso,
                "fields": {
                    "value": pressure,
                    }
                }

            ]

    return json_body

try:
    sleep_duration = float(sleep_time)
    while True:
        json_body = get_data_points()
        client.write_points(json_body)
        time.sleep(sleep_duration)

except KeyboardInterrupt:
    pass