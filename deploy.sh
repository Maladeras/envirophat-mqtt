#!/bin/bash

cd "$(dirname $0)"

apt-get -q update 
apt-get -qy install --no-install-recommends ca-certificates python python-pip python-smbus python-dev gcc python-setuptools
apt-get -qy clean all

pip install wheel
pip install rpi.gpio
pip install influxdb
pip install envirophat
#pip install paho-mqtt


cp monitor.py /usr/local/bin/monitor.py
chmod 755 /usr/local/bin/monitor.py

cp phatmon.service /etc/systemd/system/phatmon.service
chmod 755 /etc/systemd/system/phatmon.service
systemctl daemon-reload 
systemctl enable phatmon.service
